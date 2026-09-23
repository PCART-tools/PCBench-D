@_wraps(np.polydiv, lax_description=_LEADING_ZEROS_DOC)
def polydiv(u: ArrayLike, v: ArrayLike, *, trim_leading_zeros: bool = False) -> tuple[Array, Array]:
  check_arraylike("polydiv", u, v)
  u_arr, v_arr = promote_dtypes_inexact(u, v)
  m = len(u_arr) - 1
  n = len(v_arr) - 1
  scale = 1. / v_arr[0]
  q: Array = zeros(max(m - n + 1, 1), dtype = u_arr.dtype) # force same dtype
  for k in range(0, m-n+1):
    d = scale * u_arr[k]
    q = q.at[k].set(d)
    u_arr = u_arr.at[k:k+n+1].add(-d*v_arr)
  if trim_leading_zeros:
    # use the square root of finfo(dtype) to approximate the absolute tolerance used in numpy
    u_arr = trim_zeros_tol(u_arr, tol=sqrt(finfo(u_arr.dtype).eps), trim='f')
  return q, u_arr
