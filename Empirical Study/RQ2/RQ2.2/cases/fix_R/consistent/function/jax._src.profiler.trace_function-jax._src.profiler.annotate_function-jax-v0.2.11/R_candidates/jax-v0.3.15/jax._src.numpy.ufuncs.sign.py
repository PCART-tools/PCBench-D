@_wraps(np.sign, module='numpy')
@jit
def sign(x):
  _check_arraylike('sign', x)
  dtype = dtypes.dtype(x)
  if dtypes.issubdtype(dtype, np.complexfloating):
    re = lax.real(x)
    return lax.complex(
      lax.sign(_where(re != 0, re, lax.imag(x))), _constant_like(re, 0))
  return lax.sign(x)
