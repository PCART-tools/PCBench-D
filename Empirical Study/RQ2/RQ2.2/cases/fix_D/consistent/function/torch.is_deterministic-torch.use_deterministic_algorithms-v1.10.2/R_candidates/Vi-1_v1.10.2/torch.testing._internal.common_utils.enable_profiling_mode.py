@contextmanager
def enable_profiling_mode():
    old_prof_exec_state = torch._C._jit_set_profiling_executor(True)
    old_prof_mode_state = torch._C._jit_set_profiling_mode(True)
    try:
        yield
    finally:
        torch._C._jit_set_profiling_executor(old_prof_exec_state)
        torch._C._jit_set_profiling_mode(old_prof_mode_state)
