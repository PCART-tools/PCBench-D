def _pdot_transpose_rhs(g, x, y, *, axis_name, pos_contract, pos_batch, precision):
  # TODO: avals with names, call pbroadcast with axis_name
  return lax._dot_general_transpose_rhs(
      g, x, y, dimension_numbers=[pos_contract, pos_batch], precision=precision,
      preferred_element_type=None)
