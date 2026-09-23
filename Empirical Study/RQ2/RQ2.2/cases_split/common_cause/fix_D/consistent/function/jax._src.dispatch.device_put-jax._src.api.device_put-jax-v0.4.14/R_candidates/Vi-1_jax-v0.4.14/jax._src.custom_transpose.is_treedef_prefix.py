def is_treedef_prefix(entire, prefix):
  entire = tree_fill(0, entire)
  prefix = tree_fill(0, prefix)
  try:
    tree_map(lambda x, y: x, prefix, entire)
  except ValueError:
    return False
  return True
