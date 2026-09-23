@partial(jit, static_argnames=('assume_a', 'lower'))
def _solve(a: ArrayLike, b: ArrayLike, assume_a: str, lower: bool) -> Array:
  if assume_a != 'pos':
    return jnp.linalg.solve(a, b)

  a, b = _promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))
  lax_linalg._check_solve_shapes(a, b)

  # With custom_linear_solve, we can reuse the same factorization when
  # computing sensitivities. This is considerably faster.
  factors = cho_factor(lax.stop_gradient(a), lower=lower)
  custom_solve = partial(
      lax.custom_linear_solve,
      lambda x: lax_linalg._matvec_multiply(a, x),
      solve=lambda _, x: cho_solve(factors, x),
      symmetric=True)
  if a.ndim == b.ndim + 1:
    # b.shape == [..., m]
    return custom_solve(b)
  else:
    # b.shape == [..., m, k]
    return vmap(custom_solve, b.ndim - 1, max(a.ndim, b.ndim) - 1)(b)
