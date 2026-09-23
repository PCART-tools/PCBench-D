@_wraps(np.nan_to_num)
@jit
def nan_to_num(x, copy=True, nan=0.0, posinf=None, neginf=None):
  del copy
  _check_arraylike("nan_to_num", x)
  dtype = _dtype(x)
  if issubdtype(dtype, complexfloating):
    return lax.complex(
      nan_to_num(lax.real(x), nan=nan, posinf=posinf, neginf=neginf),
      nan_to_num(lax.imag(x), nan=nan, posinf=posinf, neginf=neginf))
  info = finfo(dtypes.canonicalize_dtype(dtype))
  posinf = info.max if posinf is None else posinf
  neginf = info.min if neginf is None else neginf
  x = where(isnan(x), array(nan, dtype=x.dtype), x)
  x = where(isposinf(x), array(posinf, dtype=x.dtype), x)
  x = where(isneginf(x), array(neginf, dtype=x.dtype), x)
  return x
