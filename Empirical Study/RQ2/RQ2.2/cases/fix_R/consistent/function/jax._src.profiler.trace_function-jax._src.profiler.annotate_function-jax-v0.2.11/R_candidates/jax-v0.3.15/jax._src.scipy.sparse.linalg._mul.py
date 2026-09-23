def _mul(scalar, tree):
  return tree_map(partial(operator.mul, scalar), tree)
