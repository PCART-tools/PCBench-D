def _div(tree, scalar):
  return tree_map(partial(lambda v: v / scalar), tree)
