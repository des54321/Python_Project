import threading


class SimRunner (threading.Thread):
    def __init__(self, id, work_num) -> None:
        threading.Thread.__init__(self)
        self.id = id
        self.work_num = work_num

    def run(self):
        print('hello')


thread1 = SimRunner(1,2)

thread1.start()