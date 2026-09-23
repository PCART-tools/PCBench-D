def stop():
    r"""Stops generating OS Signpost tracing from MPS backend."""
    torch._C._mps_profilerStopTrace()
