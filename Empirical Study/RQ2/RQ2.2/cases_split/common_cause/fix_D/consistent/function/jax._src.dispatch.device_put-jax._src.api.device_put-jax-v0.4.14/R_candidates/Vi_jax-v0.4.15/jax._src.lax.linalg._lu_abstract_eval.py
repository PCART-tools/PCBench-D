def _lu_abstract_eval(operand):
  operand = raise_to_shaped(operand)
  if isinstance(operand, ShapedArray):
    if operand.ndim < 2:
      raise ValueError("Argument to LU decomposition must have ndims >= 2")

    batch_dims = operand.shape[:-2]
    m = operand.shape[-2]
    n = operand.shape[-1]
    pivot = operand.update(shape=batch_dims + (min(m, n),), dtype=jnp.int32)
    perm = operand.update(shape=batch_dims + (m,), dtype=jnp.int32)
  else:
    pivot = operand
    perm = operand
  return operand, pivot, perm
