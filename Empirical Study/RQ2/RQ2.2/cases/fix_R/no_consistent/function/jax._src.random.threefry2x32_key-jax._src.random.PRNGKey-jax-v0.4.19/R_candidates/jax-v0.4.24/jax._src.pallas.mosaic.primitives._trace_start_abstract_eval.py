@trace_start_p.def_abstract_eval
def _trace_start_abstract_eval(*, message: str, level: int):
  del message, level
  return []
