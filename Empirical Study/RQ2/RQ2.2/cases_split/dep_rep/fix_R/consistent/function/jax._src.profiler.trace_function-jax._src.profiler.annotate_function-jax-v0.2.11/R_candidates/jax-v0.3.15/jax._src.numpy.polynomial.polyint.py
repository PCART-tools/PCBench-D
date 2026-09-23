@_wraps(np.polyint)
@partial(jit, static_argnames=('m',))
def polyint(p, m=1, k=None):
  m = core.concrete_or_error(operator.index, m, "'m' argument of jnp.polyint")
  k = 0 if k is None else k
  _check_arraylike("polyint", p, k)
  p, k = _promote_dtypes_inexact(p, k)
  if m < 0:
    raise ValueError("Order of integral must be positive (see polyder)")
  k = atleast_1d(k)
  if len(k) == 1:
    k = full((m,), k[0])
  if k.shape != (m,):
    raise ValueError("k must be a scalar or a rank-1 array of length 1 or m.")
  if m == 0:
    return p
  else:
    grid = (arange(len(p) + m, dtype=p.dtype)[np.newaxis]
            - arange(m, dtype=p.dtype)[:, np.newaxis])
    coeff = maximum(1, grid).prod(0)[::-1]
    return true_divide(concatenate((p, k)), coeff)
