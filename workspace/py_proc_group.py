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
      # Define shared namespace
      namespace = proc_mgr.Namespace(
        digest = 123
      )
      
      for group_idx in range(len(self.proc_groups)):
        proc_group = self.proc_groups[group_idx]

        if isinstance(proc_group, PyProcGroup):
          print(f"{self.__class__.__name__}: ProcGroup type is PyProcGroup")

          if isinstance(proc_group, PyProcGroup_Sequential):
            print(f"{self.__class__.__name__}: ProcGroup type is PyProcGroup_Sequential")
            proc_group.run()

          elif isinstance(proc_group, PyProcGroup_Concurrent):
            print(f"{self.__class__.__name__}: ProcGroup type is PyProcGroup_Concurrent")
          else:
            raise TypeError("proc_group type is unexpected")
          
        elif isinstance(proc_group, PyProc):
          print(f"{self.__class__.__name__}: ProcGroup type is PyProc")
          print(f"{self.__class__.__name__}: run(): proc[{group_idx}]: started")    
          process = multiprocessing.Process(target=proc_group.task, args=(namespace,))
          process.start()
          process.join()
          print(f"{self.__class__.__name__}: run(): proc[{group_idx}]: ended")    
          
        else:
          raise TypeError("proc_group type is unexpected")



    print(f"{self.__class__.__name__}: run(): END")    
    


class PyProcGroup_Concurrent(PyProcGroup):
  def __init__(self, proc_groups: List[PyProcGroup | PyProc]):
    super().__init__(proc_groups)

  def run(self):
    pass
