def _dot_general_transpose_rhs(g, x, *, dimension_numbers, precision,
                               preferred_element_type: Optional[DType]):
  (x_contract, y_contract), (x_batch, y_batch) = dimension_numbers
  swapped_dimension_numbers = ((y_contract, x_contract), (y_batch, x_batch))
  return _dot_general_transpose_lhs(
    g, x, dimension_numbers=swapped_dimension_numbers, precision=precision,
    preferred_element_type=preferred_element_type,
    swap_ans=True)
