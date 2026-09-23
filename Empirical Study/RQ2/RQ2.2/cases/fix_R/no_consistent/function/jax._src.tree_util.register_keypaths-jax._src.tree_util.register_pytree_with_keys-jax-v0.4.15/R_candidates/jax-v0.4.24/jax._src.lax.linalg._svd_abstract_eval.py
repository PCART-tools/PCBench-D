def _svd_abstract_eval(operand, *, full_matrices, compute_uv):
  if isinstance(operand, ShapedArray):
    if operand.ndim < 2:
      raise ValueError("Argument to singular value decomposition must have ndims >= 2")

    batch_dims = operand.shape[:-2]
    m = operand.shape[-2]
    n = operand.shape[-1]
    s = operand.update(shape=batch_dims + (min(m, n),),
                       dtype=lax_internal._complex_basetype(operand.dtype))
    if compute_uv:
      u = operand.update(shape=batch_dims + (m, m if full_matrices else min(m, n)))
      vt = operand.update(shape=batch_dims + (n if full_matrices else min(m, n), n))
      return s, u, vt
    else:
      return s,
  else:
    raise NotImplementedError
