##
# @file py_proc_mgr.py
#
# @brief Python Process Manager
#
# @subsection Features
# - Start processes sequentially
# - Start processes concurrently
# - Support repeated run in count or in loop
# - Stop processes
#
# @subsection References
# - https://superfastpython.com/multiprocessing-manager-namespace/
# - 
#
# Copyright (c) 2022 Jee Hoon Yoo.  All rights reserved.


import multiprocessing
from py_proc_group import ProcItem


class PyProcMgr:
  def __init__(self):
    self.proc_item: ProcItem = None
    self.active = False
    self.active_requested = False
    self.proc_mgr = multiprocessing.Manager()
    self.namespace = self.proc_mgr.Namespace(
      active_requested = False
    )

  def reset(self):
    if self.active:
      return

  def set(self, proc_item: ProcItem):
    self.proc_item = proc_item

  def run(self, count: int = -1):
    if self.active == True:
      return 

    if self.proc_item == None:
      return

    self.active = True
    self.active_requested = True
    self.namespace.active_requested = True

    run_count_idx = 0

    while (self.active_requested == True and (count == -1 or run_count_idx < count)): 
      self.proc_item.start(self.namespace)
      self.proc_item.join()
      if count != -1:
        run_count_idx = run_count_idx + 1

    if self.active_requested == False:
      # Run completed by counter
      self.stop()

    self.active = False
    self.namespace.active_requested = False
    self.proc_mgr.shutdown()


  def stop(self):
    if self.active == False:
      return

    self.active_requested = False
    self.namespace.active_requested = self.active_requested

  def kill(self):
    self.stop()
    self.proc_item.kill()
    
    