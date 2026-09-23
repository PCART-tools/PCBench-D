@_wraps(np.arccosh, module='numpy')
@jit
def arccosh(x: ArrayLike, /) -> Array:
  # Note: arccosh is multi-valued for complex input, and lax.acosh uses a different
  # convention than np.arccosh.
  out = lax.acosh(*_promote_args_inexact("arccosh", x))
  if dtypes.issubdtype(out.dtype, np.complexfloating):
    out = _where(real(out) < 0, lax.neg(out), out)
  return out
