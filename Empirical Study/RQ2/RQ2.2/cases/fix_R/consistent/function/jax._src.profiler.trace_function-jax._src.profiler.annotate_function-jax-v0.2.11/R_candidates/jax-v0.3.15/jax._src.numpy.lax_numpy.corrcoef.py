@_wraps(np.corrcoef)
@partial(jit, static_argnames=('rowvar',))
def corrcoef(x, y=None, rowvar=True):
  _check_arraylike("corrcoef", x)
  c = cov(x, y, rowvar)
  if len(shape(c)) == 0:
    # scalar - this should yield nan for values (nan/nan, inf/inf, 0/0), 1 otherwise
    return divide(c, c)
  d = diag(c)
  stddev = sqrt(real(d)).astype(c.dtype)
  c = c / stddev[:, None] / stddev[None, :]

  real_part = clip(real(c), -1, 1)
  if iscomplexobj(c):
    complex_part = clip(imag(c), -1, 1)
    c = lax.complex(real_part, complex_part)
  else:
    c = real_part
  return c
