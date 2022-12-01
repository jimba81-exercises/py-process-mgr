import multiprocessing
from py_proc_group import PyProcGroup


class PyProcMgr:
  def __init__(self):
    self.proc_group: PyProcGroup = None
    self.active = False

  def reset(self):
    if self.active:
      return

    self.proc_group = []

  def set(self, proc_group: PyProcGroup):
    self.proc_group = proc_group

  def run(self, count: int = -1):
    if self.active == True:
      return 

    if self.proc_group == None:
      return

    self.active = True

    with multiprocessing.Manager() as proc_mgr:
      # Define shared namespace
      namespace = proc_mgr.Namespace(
        digest = 123
      )
      self.proc_group.start(namespace)


  def stop(self):
    ...