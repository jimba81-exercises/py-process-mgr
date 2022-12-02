import multiprocessing
from typing import Any, List, Union
from abc import ABC, abstractmethod
from py_proc import PyProc


class PyProcGroup(ABC):
  def __init__(self, proc_items: List[Any]):
    self.proc_items = proc_items

  @abstractmethod
  def start(self, shared_ns, count: int, level: int) -> None:
    pass

  @abstractmethod
  def join(self) -> None:
    pass

  def kill(self) -> None:
    for proc_idx in range(len(self.proc_items)):
      proc_item = self.proc_items[proc_idx]
      proc_item.kill()


# Process Item
ProcItem = Union[PyProcGroup, PyProc]

class PyProcGroup_Sequential(PyProcGroup):
  """!
  @brief PyProcGroup for Sequential
  """  
  def __init__(self, proc_items: List[ProcItem]):
    super().__init__(proc_items)

  def start(self, shared_ns, count: int, level: int) -> None:
    if shared_ns.active_requested == False:
      return

    for proc_idx in range(len(self.proc_items)):
      proc_item = self.proc_items[proc_idx]
      proc_item.start(shared_ns, count, level + 1)
      # Current group is sequential type. Wait for each process to complete
      proc_item.join()

  def join(self) -> None:
    # Current group is sequential type. Nothing to wait.
    return


class PyProcGroup_Concurrent(PyProcGroup):
  """!
  @brief PyProcGroup for Concurrent
  """
  def __init__(self, proc_items: List[ProcItem]):
    super().__init__(proc_items)

  def start(self, shared_ns, count: int, level: int) -> None:
    if shared_ns.active_requested == False:
      return

    # Current group is concurrent type. Start all processes concurrently
    for proc_idx in range(len(self.proc_items)):
      proc_item = self.proc_items[proc_idx]
      proc_item.start(shared_ns, count, level + 1)


  def join(self) -> None:
    # Wait for all processes complete
    for proc_idx in range(len(self.proc_items)):
      proc_item = self.proc_items[proc_idx]
      proc_item.join()
    return

