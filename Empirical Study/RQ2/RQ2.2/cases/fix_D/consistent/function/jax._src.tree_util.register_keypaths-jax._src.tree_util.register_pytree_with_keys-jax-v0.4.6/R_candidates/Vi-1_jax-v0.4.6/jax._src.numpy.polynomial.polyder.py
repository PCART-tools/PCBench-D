@_wraps(np.polyder)
@partial(jit, static_argnames=('m',))
def polyder(p: Array, m: int = 1) -> Array:
  _check_arraylike("polyder", p)
  m = core.concrete_or_error(operator.index, m, "'m' argument of jnp.polyder")
  p, = _promote_dtypes_inexact(p)
  if m < 0:
    raise ValueError("Order of derivative must be positive")
  if m == 0:
    return p
  coeff = (arange(m, len(p), dtype=p.dtype)[np.newaxis]
          - arange(m, dtype=p.dtype)[:, np.newaxis]).prod(0)
  return p[:-m] * coeff[::-1]
