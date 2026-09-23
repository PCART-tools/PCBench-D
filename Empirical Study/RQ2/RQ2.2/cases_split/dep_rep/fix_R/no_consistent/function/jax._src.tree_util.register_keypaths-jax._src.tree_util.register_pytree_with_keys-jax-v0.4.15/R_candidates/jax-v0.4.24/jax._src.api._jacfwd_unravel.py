def _jacfwd_unravel(input_pytree, output_pytree_leaf, arr):
  return _unravel_array_into_pytree(
    input_pytree, -1, output_pytree_leaf, arr)
