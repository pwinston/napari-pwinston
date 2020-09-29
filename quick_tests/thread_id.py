import threading

index = 0


def get_index():
    global index
    index += 1
    return index


def report_thread_id(name, thread_id=threading.get_ident(), index=get_index()):
    print(f"{name} thread_id={thread_id} index={index}")


class MyThread(threading.Thread):
    def run(self):
        print(f"my_thread thread_id={threading.get_ident()}")
        report_thread_id("run")


report_thread_id("main")
report_thread_id("main")
my_thread = MyThread()
my_thread.start()


def func(index=get_index()):
    print(index)


func()
func()
func()
