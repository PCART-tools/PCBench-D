def _pdot_lowering(x, y, *, axis_name, pos_contract, pos_batch, precision):
  local_out = lax.dot_general(x, y, dimension_numbers=(pos_contract, pos_batch),
                              precision=precision, preferred_element_type=None)
  return psum(local_out, axis_name) if axis_name is not None else local_out
