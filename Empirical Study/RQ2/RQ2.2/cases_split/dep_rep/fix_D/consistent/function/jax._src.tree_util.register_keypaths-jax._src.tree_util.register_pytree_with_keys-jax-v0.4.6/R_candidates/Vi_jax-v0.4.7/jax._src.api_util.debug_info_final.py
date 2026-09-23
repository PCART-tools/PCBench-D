def debug_info_final(f: lu.WrappedFun, dbg: Optional[TracingDebugInfo],
                     res_paths: Callable[[], Tuple[str, ...]]) -> lu.WrappedFun:
  "Attach trace-time debug info and result paths lazy thunk to an lu.WrappedFun"
  if dbg is None: return f
  assert dbg.result_paths is None
  res_paths_ = HashableFunction(res_paths, closure=())
  return lu.add_debug_info(f, dbg._replace(result_paths=res_paths_))
