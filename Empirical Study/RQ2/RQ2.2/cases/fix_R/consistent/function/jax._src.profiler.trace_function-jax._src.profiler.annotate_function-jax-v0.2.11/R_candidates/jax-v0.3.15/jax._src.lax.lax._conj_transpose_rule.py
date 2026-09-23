def _conj_transpose_rule(t, x, *, input_dtype):
  assert ad.is_undefined_primal(x)
  if dtypes.issubdtype(input_dtype, np.complexfloating):
    return [conj(t)]
  else:
    return [real(t)]
