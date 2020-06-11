from qtpy import QtWidgets, QtCore

import numpy as np
import zarr
import vispy


class QApplicationWithTiming(QtWidgets.QApplication):
    def notify(self, receiver, event):
        return QtWidgets.QApplication.notify(self, receiver, event)


app = QApplicationWithTiming([])
QtCore.QTimer().singleShot(100, app.exit)
app.exec_()
