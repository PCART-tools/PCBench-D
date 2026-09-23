def _schur_abstract_eval(operand, *, compute_schur_vectors, sort_eig_vals,
                         select_callable):

  if operand.ndim < 2 or operand.shape[-2] != operand.shape[-1]:
    raise ValueError("Argument to Schur decomposition must have "
                     "shape [..., n, n], got shape {}".format(operand.shape))

  batch_dims = operand.shape[:-2]
  n = operand.shape[-1]
  dtype = operand.dtype
  dtype = dtypes.canonicalize_dtype(dtype)
  T = operand.update(shape=batch_dims + (n, n), dtype=dtype)
  vs = operand.update(shape=batch_dims + (n, n), dtype=dtype)

  return (T, vs) if compute_schur_vectors else (T,)
