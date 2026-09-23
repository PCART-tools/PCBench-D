@_wraps(np.polydiv, lax_description=_LEADING_ZEROS_DOC)
def polydiv(u, v, *, trim_leading_zeros=False):
  _check_arraylike("polydiv", u, v)
  u, v = _promote_dtypes_inexact(u, v)
  m = len(u) - 1
  n = len(v) - 1
  scale = 1. / v[0]
  q = zeros(max(m - n + 1, 1), dtype = u.dtype) # force same dtype
  for k in range(0, m-n+1):
    d = scale * u[k]
    q = q.at[k].set(d)
    u = u.at[k:k+n+1].add(-d*v)
  if trim_leading_zeros:
    # use the square root of finfo(dtype) to approximate the absolute tolerance used in numpy
    return q, trim_zeros_tol(u, tol=sqrt(finfo(u.dtype).eps), trim='f')
  else:
    return q, u
