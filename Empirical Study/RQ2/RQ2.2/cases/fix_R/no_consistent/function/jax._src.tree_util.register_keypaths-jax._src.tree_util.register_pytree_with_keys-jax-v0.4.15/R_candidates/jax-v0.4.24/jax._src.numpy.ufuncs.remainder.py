@implements(np.remainder, module='numpy')
@jit
def remainder(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  x1, x2 = promote_args_numeric("remainder", x1, x2)
  zero = _constant_like(x1, 0)
  if dtypes.issubdtype(x2.dtype, np.integer):
    x2 = _where(x2 == 0, lax._ones(x2), x2)
  trunc_mod = lax.rem(x1, x2)
  trunc_mod_not_zero = lax.ne(trunc_mod, zero)
  do_plus = lax.bitwise_and(
      lax.ne(lax.lt(trunc_mod, zero), lax.lt(x2, zero)), trunc_mod_not_zero)
  return lax.select(do_plus, lax.add(trunc_mod, x2), trunc_mod)
