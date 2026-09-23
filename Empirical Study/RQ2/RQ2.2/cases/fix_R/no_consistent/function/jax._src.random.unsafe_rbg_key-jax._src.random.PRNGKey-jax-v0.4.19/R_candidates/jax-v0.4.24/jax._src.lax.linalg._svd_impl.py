def _svd_impl(operand, *, full_matrices, compute_uv):
  return dispatch.apply_primitive(svd_p, operand, full_matrices=full_matrices,
                             compute_uv=compute_uv)
