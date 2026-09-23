@partial(vectorize, excluded={0, 2, 3})
def _searchsorted_via_scan(sorted_arr: Array, query: Array, side: str, dtype: type) -> Array:
  op = _sort_le_comparator if side == 'left' else _sort_lt_comparator
  def body_fun(_, state):
    low, high = state
    mid = (low + high) // 2
    go_left = op(query, sorted_arr[mid])
    return (where(go_left, low, mid), where(go_left, mid, high))
  n_levels = int(np.ceil(np.log2(len(sorted_arr) + 1)))
  init = (dtype(0), dtype(len(sorted_arr)))
  return lax.fori_loop(0, n_levels, body_fun, init)[1]
