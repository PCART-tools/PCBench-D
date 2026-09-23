def _hashable_index(idx):
  return tree_util.tree_map(
      lambda x: (x.start, x.stop) if type(x) == slice else x, idx)
