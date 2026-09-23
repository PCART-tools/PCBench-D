def _searchsorted_via_sort(sorted_arr: Array, query: Array, side: str, dtype: type) -> Array:
  working_dtype = int32 if sorted_arr.size + query.size < np.iinfo(np.int32).max else int64
  def _rank(x):
    idx = lax.iota(working_dtype, len(x))
    return zeros_like(idx).at[argsort(x)].set(idx)
  query_flat = query.ravel()
  if side == 'left':
    index = _rank(lax.concatenate([query_flat, sorted_arr], 0))[:query.size]
  else:
    index = _rank(lax.concatenate([sorted_arr, query_flat], 0))[sorted_arr.size:]
  return lax.reshape(lax.sub(index, _rank(query_flat)), np.shape(query)).astype(dtype)
