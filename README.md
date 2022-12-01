# PY Process Manager Library

## 1. Purpose
- Provides interface to manages processes excuted sequential or concurrently

## 2. Usage
```python

proc_mgr = PyProcMgr()

proc_mgr.reset()
proc_mgr.add(
  PyProc_Sequential([
    PyProc1,
    PyProc2,
    PyProc_Concurrent([
      PyProc3,
      PyProc4,
    ])
  ])
)
```