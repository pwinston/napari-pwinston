import time

for i in range(20):
    start = time.time()
    time.sleep(0.1)
    print("elapsed=%f", time.time() - start)
