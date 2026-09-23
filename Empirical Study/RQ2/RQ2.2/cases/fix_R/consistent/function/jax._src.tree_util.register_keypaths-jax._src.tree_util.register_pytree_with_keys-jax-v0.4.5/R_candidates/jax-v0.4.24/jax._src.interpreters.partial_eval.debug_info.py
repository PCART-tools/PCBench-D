def debug_info(fn: Callable, in_tree: PyTreeDef | None,
               out_tree_thunk: Callable[[], PyTreeDef] | None,
               has_kwargs: bool, traced_for: str) -> DebugInfo:
  try: sig = inspect.signature(fn)
  except (ValueError, TypeError): sig = None
  src_info = fun_sourceinfo(fn)
  return DebugInfo(src_info, sig, in_tree, out_tree_thunk, has_kwargs,
                   traced_for)
