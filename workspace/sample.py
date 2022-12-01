import time
from workspace.py_proc_group import PyProc, PyProcGroup_Sequential
from workspace.py_proc_mgr import PyProcMgr


class MyTask1(PyProc):
  def __init__(self):
    super().__init__()
    ...

  def task(self):
    print(f"{self.__class__.__name__}: Task started")
    time.sleep(2.0)
    print(f"{self.__class__.__name__}: Task Running - 1")
    time.sleep(2.0)
    print(f"{self.__class__.__name__}: Task Running - 2")
    time.sleep(1.0)
    print(f"{self.__class__.__name__}: Task Running - 3")
    time.sleep(1.0)
    print(f"{self.__class__.__name__}: Task Running - 4")
    time.sleep(1.0)
    print(f"{self.__class__.__name__}: Task ended")


class MyTask2(PyProc):
  def __init__(self):
    super().__init__()
    ...

  def task(self):
    print(f"{self.__class__.__name__}: Task started")
    time.sleep(1.0)
    print(f"{self.__class__.__name__}: Task Running - 1")
    time.sleep(1.0)
    print(f"{self.__class__.__name__}: Task Running - 2")
    time.sleep(1.0)
    print(f"{self.__class__.__name__}: Task Running - 3")
    time.sleep(2.0)
    print(f"{self.__class__.__name__}: Task Running - 4")
    time.sleep(2.0)
    print(f"{self.__class__.__name__}: Task ended")


class Main:
  def __init__(self):
    self.proc_mgr = PyProcMgr()

    my_task1 = MyTask1()

    self.proc_mgr.set(
      PyProcGroup_Sequential([
        my_task1
      ])
    )

    self.proc_mgr.run()

if __name__ == "__main__":
  Main()
  print(f">>>> MAIN END")