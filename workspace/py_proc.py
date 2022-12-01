import multiprocessing
from abc import ABC, abstractmethod

class PyProc(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def task(self, ):
    pass

  def start(self, shared_np):
    self.process = multiprocessing.Process(target=self.task, args=(shared_np,))
    self.process.start()

  def join(self):
    self.process.join()