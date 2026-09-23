@_wraps(np.gcd, module='numpy')
@jit
def gcd(x1, x2):
  _check_arraylike("gcd", x1, x2)
  if (not issubdtype(_dtype(x1), integer) or
      not issubdtype(_dtype(x2), integer)):
    raise ValueError("Arguments to jax.numpy.gcd must be integers.")
  x1, x2 = _promote_dtypes(x1, x2)
  x1, x2 = broadcast_arrays(x1, x2)
  gcd, _ = lax.while_loop(_gcd_cond_fn, _gcd_body_fn, (abs(x1), abs(x2)))
  return gcd
