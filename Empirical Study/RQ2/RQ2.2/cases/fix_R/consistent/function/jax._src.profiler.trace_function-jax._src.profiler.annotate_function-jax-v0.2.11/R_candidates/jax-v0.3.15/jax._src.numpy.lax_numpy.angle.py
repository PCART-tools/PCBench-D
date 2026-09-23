@_wraps(np.angle)
@partial(jit, static_argnames=['deg'])
def angle(z, deg=False):
  re = real(z)
  im = imag(z)
  dtype = _dtype(re)
  if not issubdtype(dtype, inexact) or (
      issubdtype(_dtype(z), floating) and ndim(z) == 0):
    dtype = dtypes.canonicalize_dtype(float_)
    re = lax.convert_element_type(re, dtype)
    im = lax.convert_element_type(im, dtype)
  result = lax.atan2(im, re)
  return degrees(result) if deg else result
