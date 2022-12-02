import multiprocessing
from abc import ABC, abstractmethod

class PyProc(ABC):
  def __init__(self):
    self.process = None

  @abstractmethod
  def task(self, shared_ns, count, level) -> None:
    pass

  def start(self, shared_ns, count: int, level: int) -> None:
    if shared_ns.active_requested == False:
      return

    self.process = multiprocessing.Process(target=self.task, args=(shared_ns,count,level))
    self.process.start()

  def join(self) -> None:
    if self.process == None:
      return
    self.process.join()
    self.process = None

  def kill(self) -> None:
    if self.process == None:
      return
    self.process.kill()
    self.process = None
