def sort_key_val(keys: Array, values: Array, dimension: int = -1,
                 is_stable: bool = True) -> Tuple[Array, Array]:
  """Sorts ``keys`` along ``dimension`` and applies the same permutation to ``values``."""
  dimension = canonicalize_axis(dimension, len(keys.shape))
  k, v = sort_p.bind(keys, values, dimension=dimension, is_stable=is_stable, num_keys=1)
  return k, v
