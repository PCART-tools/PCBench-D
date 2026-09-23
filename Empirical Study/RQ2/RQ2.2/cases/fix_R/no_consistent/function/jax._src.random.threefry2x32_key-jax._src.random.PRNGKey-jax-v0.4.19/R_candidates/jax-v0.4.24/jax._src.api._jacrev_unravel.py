def _jacrev_unravel(output_pytree, input_pytree_leaf, arr):
  return _unravel_array_into_pytree(
    output_pytree, 0, input_pytree_leaf, arr)
