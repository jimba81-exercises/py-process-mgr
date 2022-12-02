# PY Process Manager Library

## 1. Purpose
- Provides interface to manage processes executed single, sequential or concurrently

<br>

## 2. Usage

### 2.1. Init
```python
proc_mgr = PyProcMgr()
```

### 2.2. Define Process
```python
class MyProcess(PyProc):
  def __init__(self):
    super().__init__()

  # This is REQUIRED method for execute the task
  def task(self, shared_ns):
    # Do some task...
    time.sleep(2.0)

    with multiprocessing.Lock():
      # Access shared namespace with lock
      shared_ns.some_data.append(123)
      ...

```

### 2.3. Add Process Items
- Item type can be one of followings:
  - `PyProc`: Single process
  - `PyProcGroup_Sequential`: Group of processes, executed sequentially
  - `PyProcGroup_Concurrent`: Group of processes, executed concurrently
- For `PyProcGroup_Sequential`, `PyProcGroup_Concurrent`, it can have nested processes or process groups.

```python
my_task1 = MyProcess()
my_task2 = MyProcess()
my_task3 = MyProcess()
my_task4 = MyProcess()
my_task5 = MyProcess()

# Example1: Add one process
proc_mgr.set(my_task1)

# Example2: Add one process group
proc_mgr.set(
  PyProcGroup_Sequential([
    my_task1,
    my_task2
  )]
)

# Example3: Add multi-level process groups
proc_mgr.set(
  PyProcGroup_Concurrent([
    my_task1,
    PyProcGroup_Sequential([
      my_task2,
      my_task3,
      PyProcGroup_Concurrent([
        my_task4,
        my_task5,
      ]),
    ]),
  ])
)
```  

### 2.4. Run
```python
# Set namespace
proc_mgr.namespace.test_counter = 0
proc_mgr.namespace.some_data = [1,2,3,4]

# Option1: Start and run the tasks for 2 times
proc_mgr.start(count=2)

# Option2: Start and run the tasks forever
proc_mgr.start()

# Option3: Start and run the tasks forever in background thread (Non-blocking)
proc_mgr.start(run_background=True)
```

### 2.5. Stop
```python
# Option1: Stop gracefully
proc_mgr.stop()

# Option2: Kill
proc_mgr.kill()
```

<br>

## 3. TODO
### 3.1. Concurrent Processes With No-Binding
- Processes in the `PyProcGroup_Concurrent()` run concurrently and may complete in different time. However, the early completed one has to wait (*binding() is called after all processes are started*) till remaining processes to be completed. This is inevitable for **`nested`** process groups. (You really want the group to be completed if the group is a sub-group of other group)
- We may introduce `Concurrent Processes with no-binding` to the concurrent processes only if:
  - Processes are set inside `PyProcGroup_Concurrent()` class
  - The processes are the root processes (highest level of the nested groups)
  - New argument in `PyProcMgr.start()`

### 3.2. Namespace Dataclass
- Introduce `Namespace Dataclass` to write strong type support for accessing namespace data object.

### 3.3. Non-blocking PyProcMgr.start()
- Make the `PyProcMgr.start()` non-blocking so any research purpose code block can still be executed.

<br>