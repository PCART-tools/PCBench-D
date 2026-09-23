@trace_start_p.def_impl
def _trace_start_impl(*, message: str, level: int):
  del message, level
  return []
