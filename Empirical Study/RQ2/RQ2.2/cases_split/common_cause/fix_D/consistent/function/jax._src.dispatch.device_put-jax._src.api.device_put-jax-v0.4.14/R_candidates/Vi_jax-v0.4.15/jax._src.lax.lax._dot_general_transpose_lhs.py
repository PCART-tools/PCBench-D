def _dot_general_transpose_lhs(g, x, y, *, dimension_numbers, precision,
                               preferred_element_type: Optional[DTypeLike],
                               swap_ans=False):
  (x_contract, y_contract), (x_batch, y_batch) = dimension_numbers
  x_ndim = x.aval.ndim
  x_kept = remaining(range(x_ndim), x_contract, x_batch)
  y_kept = remaining(range(np.ndim(y)), y_contract, y_batch)
  if swap_ans:
    ans_batch, ans_y, _ = ranges_like(x_batch, y_kept, x_kept)
  else:
    ans_batch, _, ans_y = ranges_like(x_batch, x_kept, y_kept)
  dims = ((ans_y, y_kept), (ans_batch, y_batch))
  x_contract_sorted_by_y = list(np.take(x_contract, np.argsort(y_contract)))  # type: ignore[arg-type]
  out_axes = np.argsort(list(x_batch) + x_kept + x_contract_sorted_by_y)
  x_bar = transpose(dot_general(g, y, dims, precision=precision,
                                preferred_element_type=preferred_element_type),
                    tuple(out_axes))
  if x_bar.dtype != x.aval.dtype:
    x_bar = _convert_element_type(x_bar, x.aval.dtype, x.aval.weak_type)
  return x_bar
