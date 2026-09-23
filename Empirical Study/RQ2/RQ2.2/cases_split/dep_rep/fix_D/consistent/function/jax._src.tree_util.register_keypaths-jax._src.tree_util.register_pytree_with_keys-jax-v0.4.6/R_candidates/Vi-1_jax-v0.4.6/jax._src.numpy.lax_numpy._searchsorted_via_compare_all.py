def _searchsorted_via_compare_all(sorted_arr: Array, query: Array, side: str, dtype: type) -> Array:
  op = _sort_lt_comparator if side == 'left' else _sort_le_comparator
  comparisons = jax.vmap(op, in_axes=(0, None))(sorted_arr, query)
  return comparisons.sum(dtype=dtype, axis=0)
