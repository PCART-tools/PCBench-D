def _dot_general_transpose_rhs(g, x, y, *, dimension_numbers, precision,
                               preferred_element_type: DTypeLike | None):
  (x_contract, y_contract), (x_batch, y_batch) = dimension_numbers
  swapped_dimension_numbers = ((y_contract, x_contract), (y_batch, x_batch))
  y_bar = _dot_general_transpose_lhs(
    g, y, x, dimension_numbers=swapped_dimension_numbers, precision=precision,
    preferred_element_type=preferred_element_type,
    swap_ans=True)
  if y_bar.dtype != y.aval.dtype:
    y_bar = _convert_element_type(y_bar, y.aval.dtype, y.aval.weak_type)
  return y_bar
