import multiprocessing
from typing import Any, List, Union
from abc import ABC, abstractmethod
from py_proc import PyProc


class PyProcGroup(ABC):
  def __init__(self, proc_items: List[Any]):
    self.proc_items = proc_items

  @abstractmethod
  def start(self, shared_np) -> None:
    pass

  @abstractmethod
  def join(self) -> None:
    pass  


# Process Item
ProcItem = Union[PyProcGroup, PyProc]

class PyProcGroup_Sequential(PyProcGroup):
  def __init__(self, proc_items: List[ProcItem]):
    super().__init__(proc_items)

  def start(self, shared_np) -> None:
    print(f"{self.__class__.__name__}: start(): START")    

    for proc_idx in range(len(self.proc_items)):
      proc_item = self.proc_items[proc_idx]
      proc_item.start(shared_np)
      # Current group is sequential type. Wait for each process to complete
      proc_item.join()

    print(f"{self.__class__.__name__}: start(): END")    


  def join(self) -> None:
    # Current group is sequential type. Nothing to wait.
    return


class PyProcGroup_Concurrent(PyProcGroup):
  def __init__(self, proc_items: List[ProcItem]):
    super().__init__(proc_items)

  def start(self, shared_np) -> None:
    print(f"{self.__class__.__name__}: start(): START")    

    # Current group is concurrent type. Start all processes concurrently
    for proc_idx in range(len(self.proc_items)):
      proc_item = self.proc_items[proc_idx]
      proc_item.start(shared_np)



    print(f"{self.__class__.__name__}: start(): END")    


  def join(self) -> None:
    # Wait for all processes complete
    for proc_idx in range(len(self.proc_items)):
      proc_item = self.proc_items[proc_idx]
      proc_item.join()
    return
