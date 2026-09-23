def tree_fill(x, treedef):
  return tree_unflatten(treedef, [x] * treedef.num_leaves)
