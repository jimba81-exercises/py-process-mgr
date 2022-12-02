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

  def task(self, shared_ns, count: int, level: int) -> None:
  """!
  @brief This is MUST HAVE and the task Work method
  @param shared_ns: Shared namespace with all processes
  @param count: Number of count that the task has been executed
  @param level: Task group level (root=0)
  """
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

#### 2.4.1. Run Options:
- `count_max`: number of count that each task shall be executed. If **-1**, tasks run forever *(Default=-1)*
- `run_background`: Run tasks in background thread *(Default=False)*
- `skip_binding`: If root group is `PyProcGroup_Concurrent` and `skip_binding` is set to False, each task shall NOT wait for other task to complete in each cycle. *(Default=False)*

#### 2.4.2. Examples:

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

# Option4: Start and run the tasks forever without binding (No wait for other process to complete)
#          For skip binding to work, root group type SHOULD be PyProcGroup_Concurrent
proc_mgr.start(skip_binding=True)
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

### 3.1. Namespace Dataclass
- Introduce `Namespace Dataclass` to write strong type support for accessing namespace data object.

<br>