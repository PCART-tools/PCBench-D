@implements(np.arccosh, module='numpy')
@jit
def arccosh(x: ArrayLike, /) -> Array:
  # Note: arccosh is multi-valued for complex input, and lax.acosh
  # uses a different convention than np.arccosh.
  result = lax.acosh(*promote_args_inexact("arccosh", x))
  if dtypes.issubdtype(result.dtype, np.complexfloating):
    result = _where(real(result) < 0, lax.neg(result), result)
  return result
