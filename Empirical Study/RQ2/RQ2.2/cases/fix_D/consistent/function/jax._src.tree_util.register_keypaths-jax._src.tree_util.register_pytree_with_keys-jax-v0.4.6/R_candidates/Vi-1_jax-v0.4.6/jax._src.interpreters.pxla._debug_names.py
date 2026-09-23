def _debug_names(
    dbg: Optional[core.DebugInfo], kept_var_idx: Optional[Set] = None
) -> Tuple[Optional[List[str]], Optional[List[str]]]:
  if dbg is None: return (None, None)
  arg_info = pe.arg_info_all(dbg)
  arg_names = None if arg_info is None else [
      f'{name}{keystr(path)}' for i, (name, path) in enumerate(arg_info)
      if kept_var_idx is None or i in kept_var_idx]
  result_info = pe.result_info(dbg)
  result_names = None if result_info is None else map(keystr, result_info)
  return arg_names, result_names
