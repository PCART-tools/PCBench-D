@_wraps(np.rint, module='numpy')
@jit
def rint(x: ArrayLike, /) -> Array:
  check_arraylike('rint', x)
  dtype = dtypes.dtype(x)
  if dtype == bool or dtypes.issubdtype(dtype, np.integer):
    return lax.convert_element_type(x, dtypes.float_)
  if dtypes.issubdtype(dtype, np.complexfloating):
    return lax.complex(rint(lax.real(x)), rint(lax.imag(x)))
  return lax.round(x, lax.RoundingMethod.TO_NEAREST_EVEN)
