@implements(np.hypot, module='numpy')
@jit
def hypot(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  x1, x2 = promote_args_inexact("hypot", x1, x2)

  # TODO(micky774): Promote to ValueError when deprecation is complete
  # (began 2024-4-14).
  if dtypes.issubdtype(x1.dtype, np.complexfloating):
    deprecations.warn(
      "jax-numpy-hypot-complex",
      "Passing complex-valued inputs to hypot is deprecated and will raise a "
      "ValueError in the future. Please convert to real values first, such as "
      "by using jnp.real or jnp.imag to take the real or imaginary components "
      "respectively.",
      stacklevel=2)
  x1, x2 = lax.abs(x1), lax.abs(x2)
  idx_inf = lax.bitwise_or(isposinf(x1), isposinf(x2))
  x1, x2 = maximum(x1, x2), minimum(x1, x2)
  x = _where(x1 == 0, x1, x1 * lax.sqrt(1 + lax.square(lax.div(x2, _where(x1 == 0, lax._ones(x1), x1)))))
  return _where(idx_inf, _lax_const(x, np.inf), x)
