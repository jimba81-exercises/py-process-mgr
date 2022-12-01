import multiprocessing
from typing import Any, List, Union
from abc import ABC, abstractmethod

class PyProc(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def task(self):
    pass
  

class PyProcGroup(ABC):
  def __init__(self, proc_groups: List[Any]):
    self.proc_groups = proc_groups

  @abstractmethod
  def run(self):
    pass


class PyProcGroup_Sequential(PyProcGroup):
  def __init__(self, proc_groups: List[Union[PyProcGroup, PyProc]]):
    super().__init__(proc_groups)

  def run(self):
    print(f"{self.__class__.__name__}: run(): START")    

    with multiprocessing.Manager() as proc_mgr:
      namespace = proc_mgr.Namespace()
      for proc_group in self.proc_groups:
        process = multiprocessing.Process(target=proc_group.task, args=(namespace,))
        process.start()
        process.join()

    print(f"{self.__class__.__name__}: run(): END")    
    


class PyProcGroup_Concurrent(PyProcGroup):
  def __init__(self, proc_groups: List[PyProcGroup | PyProc]):
    super().__init__(proc_groups)

  def run(self):
    pass
