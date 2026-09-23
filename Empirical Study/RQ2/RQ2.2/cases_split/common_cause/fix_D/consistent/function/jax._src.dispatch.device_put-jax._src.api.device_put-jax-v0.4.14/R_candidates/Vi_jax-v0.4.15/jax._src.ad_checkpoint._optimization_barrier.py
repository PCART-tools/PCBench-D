def _optimization_barrier(arg):
  flat_args, treedef = tree_flatten(arg)
  return tree_unflatten(treedef, optimization_barrier_p.bind(*flat_args))
