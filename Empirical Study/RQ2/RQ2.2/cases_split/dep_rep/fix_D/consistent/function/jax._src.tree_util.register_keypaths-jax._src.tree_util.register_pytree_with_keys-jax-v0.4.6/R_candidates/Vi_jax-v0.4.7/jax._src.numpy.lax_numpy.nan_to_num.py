@util._wraps(np.nan_to_num)
@jit
def nan_to_num(x: ArrayLike, copy: bool = True, nan: ArrayLike = 0.0,
               posinf: Optional[ArrayLike] = None,
               neginf: Optional[ArrayLike] = None) -> Array:
  del copy
  util.check_arraylike("nan_to_num", x)
  dtype = _dtype(x)
  if not issubdtype(dtype, inexact):
    return asarray(x)
  if issubdtype(dtype, complexfloating):
    return lax.complex(
      nan_to_num(lax.real(x), nan=nan, posinf=posinf, neginf=neginf),
      nan_to_num(lax.imag(x), nan=nan, posinf=posinf, neginf=neginf))
  info = finfo(dtypes.canonicalize_dtype(dtype))
  posinf = info.max if posinf is None else posinf
  neginf = info.min if neginf is None else neginf
  out = where(ufuncs.isnan(x), asarray(nan, dtype=dtype), x)
  out = where(ufuncs.isposinf(out), asarray(posinf, dtype=dtype), out)
  out = where(ufuncs.isneginf(out), asarray(neginf, dtype=dtype), out)
  return out
