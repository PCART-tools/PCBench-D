@partial(jit, static_argnames=('lower',))
def _cho_solve(c: ArrayLike, b: ArrayLike, lower: bool) -> Array:
  c, b = promote_dtypes_inexact(jnp.asarray(c), jnp.asarray(b))
  lax_linalg._check_solve_shapes(c, b)
  b = lax_linalg.triangular_solve(c, b, left_side=True, lower=lower,
                                  transpose_a=not lower, conjugate_a=not lower)
  b = lax_linalg.triangular_solve(c, b, left_side=True, lower=lower,
                                  transpose_a=lower, conjugate_a=lower)
  return b
