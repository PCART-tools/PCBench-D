def _pp_slice(context: core.JaxprPpContext, dim, slc: indexing.Slice
              ) -> str:
  start, size = slc.start, slc.size
  if isinstance(start, core.Var):
    start_str = core.pp_var(start, context)
    end_str = f'{start_str}+{size}'
  else:
    start_str = '' if start == 0 else str(start)
    end = start + size
    end_str = '' if end == dim else str(end)
  return f'{start_str}:{end_str}'
