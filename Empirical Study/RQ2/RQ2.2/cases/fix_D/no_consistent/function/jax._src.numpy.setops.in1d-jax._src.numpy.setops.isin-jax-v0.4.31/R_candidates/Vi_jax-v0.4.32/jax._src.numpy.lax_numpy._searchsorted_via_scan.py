@partial(vectorize, excluded={0, 1, 3, 4})
def _searchsorted_via_scan(unrolled: bool, sorted_arr: Array, query: Array, side: str, dtype: type) -> Array:
  op = _sort_le_comparator if side == 'left' else _sort_lt_comparator
  def body_fun(state, _):
    low, high = state
    mid = (low + high) // 2
    go_left = op(query, sorted_arr[mid])
    return (where(go_left, low, mid), where(go_left, mid, high)), ()
  n_levels = int(np.ceil(np.log2(len(sorted_arr) + 1)))
  init = (dtype(0), dtype(len(sorted_arr)))
  carry, _ = lax.scan(body_fun, init, (), length=n_levels,
                      unroll=n_levels if unrolled else 1)
  return carry[1]
