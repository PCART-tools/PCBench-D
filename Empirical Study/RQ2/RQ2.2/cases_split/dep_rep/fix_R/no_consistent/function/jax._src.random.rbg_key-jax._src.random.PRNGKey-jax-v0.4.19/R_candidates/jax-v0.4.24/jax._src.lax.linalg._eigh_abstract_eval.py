def _eigh_abstract_eval(operand, *, lower, sort_eigenvalues, subset_by_index):
  if isinstance(operand, ShapedArray):
    if operand.ndim < 2 or operand.shape[-2] != operand.shape[-1]:
      raise ValueError(
        "Argument to symmetric eigendecomposition must have shape [..., n, n],"
        "got shape {}".format(operand.shape))

    batch_dims = operand.shape[:-2]
    n = operand.shape[-1]
    d = (
        n
        if subset_by_index is None
        else subset_by_index[1] - subset_by_index[0]
    )
    v = operand.update(shape=batch_dims + (n, d))
    w = operand.update(
        shape=batch_dims + (d,),
        dtype=lax_internal._complex_basetype(operand.dtype),
    )
  else:
    v, w = operand, operand
  return v, w
