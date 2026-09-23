@_wraps(np.copysign, module='numpy')
@jit
def copysign(x1, x2):
  x1, x2 = _promote_args_inexact("copysign", x1, x2)
  if dtypes.issubdtype(dtypes.dtype(x1), np.complexfloating):
    raise TypeError("copysign does not support complex-valued inputs")
  return _where(signbit(x2).astype(bool), -lax.abs(x1), lax.abs(x1))
