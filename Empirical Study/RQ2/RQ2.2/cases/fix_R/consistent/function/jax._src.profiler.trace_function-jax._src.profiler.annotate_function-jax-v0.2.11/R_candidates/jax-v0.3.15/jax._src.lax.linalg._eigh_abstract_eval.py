def _eigh_abstract_eval(operand, *, lower, sort_eigenvalues):
  if isinstance(operand, ShapedArray):
    if operand.ndim < 2 or operand.shape[-2] != operand.shape[-1]:
      raise ValueError(
        "Argument to symmetric eigendecomposition must have shape [..., n, n],"
        "got shape {}".format(operand.shape))

    batch_dims = operand.shape[:-2]
    n = operand.shape[-1]
    v = operand.update(shape=batch_dims + (n, n))
    w = operand.update(shape=batch_dims + (n,),
                       dtype=lax_internal._complex_basetype(operand.dtype))
  else:
    v, w = operand, operand
  return v, w
