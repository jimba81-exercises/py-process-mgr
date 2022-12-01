import multiprocessing
from typing import List
from workspace.py_proc_group import PyProcGroup


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

  def run(self):
    if self.active == True:
      return 

    if self.proc_group == None:
      return

    self.active = True
    self.proc_group.run()


  def stop(self):
    ...