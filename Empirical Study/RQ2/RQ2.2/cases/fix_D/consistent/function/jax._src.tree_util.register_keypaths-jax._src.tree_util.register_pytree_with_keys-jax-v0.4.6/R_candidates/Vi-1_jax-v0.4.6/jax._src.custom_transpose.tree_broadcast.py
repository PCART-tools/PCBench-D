def tree_broadcast(full_treedef, tree, is_leaf=None):
  full_tree = tree_fill(0, full_treedef)
  return tree_map(tree_fill_like, tree, full_tree, is_leaf=is_leaf)
