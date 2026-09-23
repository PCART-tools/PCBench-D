def _slice_tile(x, dim: Optional[int], i, n: int):
  """Selects an `i`th (out of `n`) tiles of `x` along `dim`."""
  if dim is None: return x
  (tile_size, rem) = divmod(x.shape[dim], n)
  assert rem == 0, "Please open a bug report!"
  return lax.dynamic_slice_in_dim(x, i * tile_size, slice_size=tile_size, axis=dim)
