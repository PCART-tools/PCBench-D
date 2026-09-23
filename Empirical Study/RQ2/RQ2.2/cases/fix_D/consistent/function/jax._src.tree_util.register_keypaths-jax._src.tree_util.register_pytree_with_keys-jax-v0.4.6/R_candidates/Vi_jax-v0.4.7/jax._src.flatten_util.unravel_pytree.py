def unravel_pytree(treedef, unravel_list, flat):
  return tree_unflatten(treedef, unravel_list(flat))
