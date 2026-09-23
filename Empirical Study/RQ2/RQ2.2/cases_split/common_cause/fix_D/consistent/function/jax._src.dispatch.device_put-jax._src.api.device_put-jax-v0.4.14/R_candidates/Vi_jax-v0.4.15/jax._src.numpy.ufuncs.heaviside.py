@_wraps(np.heaviside, module='numpy')
@jit
def heaviside(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  check_arraylike("heaviside", x1, x2)
  x1, x2 = promote_dtypes_inexact(x1, x2)
  zero = _lax_const(x1, 0)
  return _where(lax.lt(x1, zero), zero,
                _where(lax.gt(x1, zero), _lax_const(x1, 1), x2))
