def sig_info(dbg: DebugInfo) -> inspect.BoundArguments | None:
  if dbg.in_tree is None or dbg.signature is None: return None
  try:
    dummy_args = tree_unflatten(dbg.in_tree, [False] * dbg.in_tree.num_leaves)
  except:
    return None
  args, kwargs = dummy_args if dbg.has_kwargs else (dummy_args, {})
  try:
    return dbg.signature.bind(*args, **kwargs)
  except (TypeError, ValueError):
    return None
