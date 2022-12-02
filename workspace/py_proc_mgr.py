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
import threading
from py_proc_group import ProcItem, PyProcGroup_Concurrent


class PyProcMgr:
  def __init__(self):
    self.proc_item: ProcItem = None
    self.active = False
    self.active_requested = False
    self.proc_mgr = multiprocessing.Manager()
    self.namespace = self.proc_mgr.Namespace(
      active_requested = False
    )

  def set(self, proc_item: ProcItem):
    self.proc_item = proc_item

  def start(self, count_max: int = -1, run_background: bool = False, skip_binding: bool = False) -> None:
    if self.active == True:
      return 

    if self.proc_item == None:
      return

    if run_background == True:
      # Run in a thread
      self._run_thread = threading.Thread(target=self._start, args=(count_max,skip_binding))
      self._run_thread.start()
    else:
      self._start(count_max, skip_binding)


  def stop(self):
    if self.active == False:
      return

    self.active_requested = False
    self.namespace.active_requested = self.active_requested

  def kill(self):
    self.stop()
    self.proc_item.kill()
    

  def _start(self, count_max: int, skip_binding: bool):
    self.active = True
    self.active_requested = True
    self.namespace.active_requested = True

    if skip_binding == True:
      self._start_with_no_binding(count_max)
    else:
      self._start_with_binding(count_max)


  def _run_proc_item(self, proc_item: ProcItem, namespace, count_max):
    run_count_idx = 0
    while (namespace.active_requested == True and (count_max == -1 or run_count_idx < count_max)):
      proc_item.start(shared_ns=self.namespace, count=run_count_idx, level=0)
      proc_item.join()
      run_count_idx = run_count_idx + 1    

  def _start_with_binding(self, count_max: int):
    self._run_proc_item(proc_item=self.proc_item, namespace=self.namespace, count_max=count_max)

    if self.active_requested == False:
      # Run completed by counter
      self.stop()

    self.active = False
    self.namespace.active_requested = False
    self.proc_mgr.shutdown()


  def _start_with_no_binding(self, count_max: int):
    # Skip binding is only supported when all below conditions are met:
    # - Root group type is PyProcGroup_Concurrent

    if isinstance(self.proc_item, PyProcGroup_Concurrent) == False:
      raise Exception(f"Unexpected Process Group Type: Expected type=({PyProcGroup_Concurrent})")

    # Run each process group in separate process (callin ProcGroup process)
    processes = []
    for proc_idx in range(len(self.proc_item.proc_items)):
      proc_item = self.proc_item.proc_items[proc_idx]
      process = multiprocessing.Process(target=self._run_proc_item, args=(proc_item,self.namespace,count_max))
      processes.append(process)
      #print(f"Skip_Binding Process started: pid={processes[proc_idx].pid}")
      processes[proc_idx].start()

    # Wait until all 'ProcGroup' processes are completed
    for proc_idx in range(len(processes)):
      process = processes[proc_idx]
      process.join()

