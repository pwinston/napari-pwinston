#!/usr/bin/env python

# get_ipython().run_line_magic('gui', 'qt')

import sys

sys.path.append("..")

import numpy as np

from torchvision.datasets import MNIST
from torchvision import transforms
from torch.utils.data import Dataset

from napari.utils import resize_dask_cache

resize_dask_cache(0)

mnist_train = MNIST(
    '../data/MNIST',
    download=True,
    transform=transforms.Compose([transforms.ToTensor(),]),
    train=True,
)

mnist_test = MNIST(
    '../data/MNIST',
    download=True,
    transform=transforms.Compose([transforms.ToTensor(),]),
    train=False,
)

from torch import randn


def add_noise(img):
    return img + randn(img.size()) * 0.4


class SyntheticNoiseDataset(Dataset):
    def __init__(self, data, mode='train'):
        self.mode = mode
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        img = self.data[index][0]
        return add_noise(img), img


noisy_mnist_train = SyntheticNoiseDataset(mnist_train, 'train')
noisy_mnist_test = SyntheticNoiseDataset(mnist_test, 'test')


noisy, clean = noisy_mnist_train[0]
# plot_tensors([noisy[0], clean[0]], ['Noisy Image', 'Clean Image'])


# from mask import Masker

# masker = Masker(width=4, mode='interpolate')

# net_input, mask = masker.mask(noisy.unsqueeze(0), 0)

# plot_tensors(
#    [mask, noisy[0], net_input[0], net_input[0] - noisy[0]],
#    ["Mask", "Noisy Image", "Neural Net Input", "Difference"],
# )

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        dropout=False,
        norm='batch',
        residual=True,
        activation='leakyrelu',
        transpose=False,
    ):
        super(ConvBlock, self).__init__()
        self.dropout = dropout
        self.residual = residual
        self.activation = activation
        self.transpose = transpose

        if self.dropout:
            self.dropout1 = nn.Dropout2d(p=0.05)
            self.dropout2 = nn.Dropout2d(p=0.05)

        self.norm1 = None
        self.norm2 = None
        if norm == 'batch':
            self.norm1 = nn.BatchNorm2d(out_channels)
            self.norm2 = nn.BatchNorm2d(out_channels)
        elif norm == 'instance':
            self.norm1 = nn.InstanceNorm2d(out_channels, affine=True)
            self.norm2 = nn.InstanceNorm2d(out_channels, affine=True)
        elif norm == 'mixed':
            self.norm1 = nn.BatchNorm2d(out_channels, affine=True)
            self.norm2 = nn.InstanceNorm2d(out_channels, affine=True)

        if self.transpose:
            self.conv1 = nn.ConvTranspose2d(
                in_channels, out_channels, kernel_size=3, padding=1
            )
            self.conv2 = nn.ConvTranspose2d(
                out_channels, out_channels, kernel_size=3, padding=1
            )
        else:
            self.conv1 = nn.Conv2d(
                in_channels, out_channels, kernel_size=3, padding=1
            )
            self.conv2 = nn.Conv2d(
                out_channels, out_channels, kernel_size=3, padding=1
            )

        if self.activation == 'relu':
            self.actfun1 = nn.ReLU()
            self.actfun2 = nn.ReLU()
        elif self.activation == 'leakyrelu':
            self.actfun1 = nn.LeakyReLU()
            self.actfun2 = nn.LeakyReLU()
        elif self.activation == 'elu':
            self.actfun1 = nn.ELU()
            self.actfun2 = nn.ELU()
        elif self.activation == 'selu':
            self.actfun1 = nn.SELU()
            self.actfun2 = nn.SELU()

    def forward(self, x):
        ox = x

        x = self.conv1(x)

        if self.dropout:
            x = self.dropout1(x)

        if self.norm1:
            x = self.norm1(x)

        x = self.actfun1(x)

        x = self.conv2(x)

        if self.dropout:
            x = self.dropout2(x)

        if self.norm2:
            x = self.norm2(x)

        if self.residual:
            x[:, 0 : min(ox.shape[1], x.shape[1]), :, :] += ox[
                :, 0 : min(ox.shape[1], x.shape[1]), :, :
            ]

        x = self.actfun2(x)

        # print("shapes: x:%s ox:%s " % (x.shape,ox.shape))

        return x


class BabyUnet(nn.Module):
    def __init__(self, n_channel_in=1, n_channel_out=1, width=16):
        super(BabyUnet, self).__init__()
        self.pool1 = nn.MaxPool2d(kernel_size=2)
        self.pool2 = nn.MaxPool2d(kernel_size=2)

        self.up1 = lambda x: F.interpolate(
            x, mode='bilinear', scale_factor=2, align_corners=False
        )
        self.up2 = lambda x: F.interpolate(
            x, mode='bilinear', scale_factor=2, align_corners=False
        )

        self.conv1 = ConvBlock(n_channel_in, width)
        self.conv2 = ConvBlock(width, 2 * width)

        self.conv3 = ConvBlock(2 * width, 2 * width)

        self.conv4 = ConvBlock(4 * width, 2 * width)
        self.conv5 = ConvBlock(3 * width, width)

        self.conv6 = nn.Conv2d(width, n_channel_out, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        x = self.pool1(c1)
        c2 = self.conv2(x)
        x = self.pool2(c2)
        x = self.conv3(x)

        x = self.up1(x)
        x = torch.cat([x, c2], 1)
        x = self.conv4(x)
        x = self.up2(x)
        x = torch.cat([x, c1], 1)
        x = self.conv5(x)
        x = self.conv6(x)
        return x


model = BabyUnet()

from torch.nn import MSELoss
from torch.optim import Adam
from torch.utils.data import DataLoader

loss_function = MSELoss()
optimizer = Adam(model.parameters(), lr=0.001)


import dask
import dask.array as da

num_tests = len(noisy_mnist_test)

noisy_test_dask = da.stack(
    [
        da.from_delayed(
            dask.delayed(lambda i: noisy_mnist_test[i][0].detach().numpy())(i),
            shape=(1, 28, 28),
            dtype=np.float32,
        ).reshape((28, 28))
        for i in range(num_tests)
    ]
)

clean_test_dask = da.stack(
    [
        da.from_delayed(
            dask.delayed(lambda i: noisy_mnist_test[i][1].detach().numpy())(i),
            shape=(1, 28, 28),
            dtype=np.float32,
        ).reshape((28, 28))
        for i in range(num_tests)
    ]
)

import torch


def test_numpy_to_result_numpy(i):
    """Convert test NumPy array to model output and back to NumPy."""
    out = (
        model(torch.Tensor(np.array(noisy_test_dask[i : i + 1, np.newaxis])))
        .detach()
        .numpy()
        .squeeze()
    )
    return out


# build the results dask array
model_output_dask = da.stack(
    [
        da.from_delayed(
            dask.delayed(test_numpy_to_result_numpy)(i),
            shape=(28, 28),
            dtype=np.float32,
        )
        for i in range(len(noisy_mnist_test))
    ]
)

from napari.utils.perf import perf_timer


import napari


def main():
    with napari.gui_qt():
        clean = np.array(clean_test_dask)
        noisy = np.array(noisy_test_dask)
        viewer = napari.Viewer()
        _ = viewer.add_image(clean)  # returns layer, we don't care
        _ = viewer.add_image(noisy)
        model_layer = viewer.add_image(
            model_output_dask,
            contrast_limits=(
                np.min(noisy_test_dask[0:10]).compute(),
                np.max(noisy_test_dask[0:10]).compute(),
            ),
        )  # this layer though, we're gonna play with
        viewer.grid_view()


if __name__ == '__main__':
    main()
