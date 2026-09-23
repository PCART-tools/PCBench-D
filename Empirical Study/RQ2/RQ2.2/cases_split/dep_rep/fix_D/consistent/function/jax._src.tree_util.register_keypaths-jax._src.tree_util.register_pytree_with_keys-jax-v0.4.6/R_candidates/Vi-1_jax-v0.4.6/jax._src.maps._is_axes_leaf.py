def _is_axes_leaf(entry):
  if isinstance(entry, dict) and all_leaves(entry.values()):
    return True
  # NOTE: `None`s are not considered leaves by `all_leaves`
  if isinstance(entry, (tuple, list)) and all_leaves(v for v in entry if v is not None):
    return True
  return False
