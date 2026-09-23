@_wraps(np.ldexp, module='numpy')
@jit
def ldexp(x1, x2):
  _check_arraylike("ldexp", x1, x2)
  x1_dtype = dtypes.dtype(x1)
  x2_dtype = dtypes.dtype(x2)
  if (dtypes.issubdtype(x1_dtype, np.complexfloating)
      or dtypes.issubdtype(x2_dtype, np.inexact)):
    raise ValueError(f"ldexp not supported for input types {(x1_dtype, x2_dtype)}")

  x1, x2 = _promote_shapes("ldexp", x1, x2)

  dtype = dtypes.canonicalize_dtype(dtypes._to_inexact_dtype(x1_dtype))
  info = dtypes.finfo(dtype)
  int_type = _INT_DTYPES[info.bits]

  x1 = lax.convert_element_type(x1, dtype)
  x2 = lax.convert_element_type(x2, int_type)

  mask = (1 << info.nexp) - 1
  bias = ((1 << info.nexp) - 1) >> 1
  x, e = _normalize_float(x1)
  x2 += e + ((x >> info.nmant) & mask) - bias

  # find underflow/overflow before denormalization
  underflow_cond = x2 < -(bias + info.nmant)
  overflow_cond = x2 > bias

  m = lax.full_like(x, 1, dtype=dtype)

  # denormals
  cond = x2 < -bias + 1
  x2 = _where(cond, x2 + info.nmant, x2)
  m = _where(cond, m / (1 << info.nmant), m)

  x2 = lax.convert_element_type(x2, np.int32)
  x &= ~(mask << info.nmant)
  x |= ((lax.convert_element_type(x2, int_type) + bias) << info.nmant)

  x = lax.convert_element_type(m, dtype) * lax.bitcast_convert_type(x, dtype)

  # underflow
  x = _where(underflow_cond, lax.full_like(x, 0, dtype=dtype), x)
  # overflow
  x = _where(overflow_cond, lax.sign(x1) * lax.full_like(x, np.inf), x)
  # ldexp(x1, x2) = x1 for x1 = inf, -inf, nan, 0
  return _where(isinf(x1) | isnan(x1) | (x1 == 0), x1, x)
