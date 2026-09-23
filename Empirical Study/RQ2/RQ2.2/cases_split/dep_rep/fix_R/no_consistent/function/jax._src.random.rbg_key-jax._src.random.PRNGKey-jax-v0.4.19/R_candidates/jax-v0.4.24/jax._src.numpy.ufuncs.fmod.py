@implements(np.fmod, module='numpy')
@jit
def fmod(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  check_arraylike("fmod", x1, x2)
  if dtypes.issubdtype(dtypes.result_type(x1, x2), np.integer):
    x2 = _where(x2 == 0, lax._ones(x2), x2)
  return lax.rem(*promote_args_numeric("fmod", x1, x2))
