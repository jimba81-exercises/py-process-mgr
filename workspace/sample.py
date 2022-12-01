import time
from py_proc_group import PyProc, PyProcGroup_Concurrent, PyProcGroup_Sequential
from py_proc_mgr import PyProcMgr


class MyTask1(PyProc):
  def __init__(self):
    super().__init__()
    ...

  def task(self, shared_ns):
    print(f"{self.__class__.__name__}: Task started")
    time.sleep(3.0)
    print(f"{self.__class__.__name__}: Task Running - 1")
    time.sleep(3.0)
    print(f"{self.__class__.__name__}: Task Running - 2")
    time.sleep(3.0)
    print(f"{self.__class__.__name__}: Task Running - 3")
    time.sleep(3.0)
    print(f"{self.__class__.__name__}: Task ended")


class MyTask2(PyProc):
  def __init__(self):
    super().__init__()
    ...

  def task(self, shared_ns):
    print(f"{self.__class__.__name__}: Task started")
    time.sleep(1.5)
    print(f"{self.__class__.__name__}: Task Running - 1")
    time.sleep(1.5)
    print(f"{self.__class__.__name__}: Task Running - 2")
    time.sleep(1.5)
    print(f"{self.__class__.__name__}: Task ended")

class MyTask3(PyProc):
  def __init__(self):
    super().__init__()
    ...

  def task(self, shared_ns):
    print(f"{self.__class__.__name__}: Task started")
    time.sleep(0.5)
    print(f"{self.__class__.__name__}: Task Running - 1")
    time.sleep(0.5)
    print(f"{self.__class__.__name__}: Task Running - 2")
    time.sleep(0.5)
    print(f"{self.__class__.__name__}: Task ended")

class MyTask4(PyProc):
  def __init__(self):
    super().__init__()
    ...

  def task(self, shared_ns):
    print(f"{self.__class__.__name__}: Task started")
    time.sleep(0.5)
    print(f"{self.__class__.__name__}: Task Running - 1")
    time.sleep(0.5)
    print(f"{self.__class__.__name__}: Task Running - 2")
    time.sleep(0.5)
    print(f"{self.__class__.__name__}: Task ended")

class MyTask5(PyProc):
  def __init__(self):
    super().__init__()
    ...

  def task(self, shared_ns):
    print(f"{self.__class__.__name__}: Task started")
    time.sleep(0.2)
    print(f"{self.__class__.__name__}: Task Running - 1")
    time.sleep(0.2)
    print(f"{self.__class__.__name__}: Task Running - 2")
    time.sleep(0.2)
    print(f"{self.__class__.__name__}: Task ended")

class Main:
  def __init__(self):
    self.proc_mgr = PyProcMgr()

    my_task1 = MyTask1()
    my_task2 = MyTask2()
    my_task3 = MyTask3()
    my_task4 = MyTask4()
    my_task5 = MyTask5()

    self.proc_mgr.set(
      PyProcGroup_Sequential([
        my_task1,
        PyProcGroup_Sequential([
          my_task2,
          my_task2
        ]),
        my_task1
      ])
    )

    self.proc_mgr.set(
      PyProcGroup_Concurrent([
        my_task1,
        PyProcGroup_Sequential([
          my_task2,
          my_task3,
          PyProcGroup_Concurrent([
            my_task4,
            my_task5,
        ]),
        ]),
      ])
    )

    self.proc_mgr.run()

if __name__ == "__main__":
  Main()
  print(f">>>> MAIN END")