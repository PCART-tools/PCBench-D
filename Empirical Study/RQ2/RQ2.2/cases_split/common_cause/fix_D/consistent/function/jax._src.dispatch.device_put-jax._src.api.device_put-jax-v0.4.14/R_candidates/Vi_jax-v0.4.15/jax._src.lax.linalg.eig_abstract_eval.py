def eig_abstract_eval(operand, *, compute_left_eigenvectors,
                      compute_right_eigenvectors):
  if isinstance(operand, ShapedArray):
    if operand.ndim < 2 or operand.shape[-2] != operand.shape[-1]:
      raise ValueError("Argument to nonsymmetric eigendecomposition must have "
                       "shape [..., n, n], got shape {}".format(operand.shape))

    batch_dims = operand.shape[:-2]
    n = operand.shape[-1]
    dtype = np.complex64 if dtypes.finfo(operand.dtype).bits == 32 else np.complex128
    dtype = dtypes.canonicalize_dtype(dtype)
    vl = vr = operand.update(shape=batch_dims + (n, n), dtype=dtype)
    w = operand.update(shape=batch_dims + (n,), dtype=dtype)
  else:
    raise NotImplementedError

  output = [w]
  if compute_left_eigenvectors:
    output.append(vl)
  if compute_right_eigenvectors:
    output.append(vr)

  return tuple(output)
