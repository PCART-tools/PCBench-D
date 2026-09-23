def result_info(dbg: DebugInfo) -> list[KeyPath] | None:
  if dbg.out_tree is None: return None
  try:
    num_leaves = dbg.out_tree().num_leaves
    dummy_result = tree_unflatten(dbg.out_tree(), [False] * num_leaves)
  except:
    return None
  else:
    return [path for path, _ in generate_key_paths(dummy_result)]
