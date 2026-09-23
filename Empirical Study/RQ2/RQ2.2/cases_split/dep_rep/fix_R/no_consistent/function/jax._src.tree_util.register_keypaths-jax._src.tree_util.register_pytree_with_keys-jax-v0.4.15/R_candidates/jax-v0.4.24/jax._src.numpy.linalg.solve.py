@implements(np.linalg.solve)
@jit
def solve(a: ArrayLike, b: ArrayLike) -> Array:
  check_arraylike("jnp.linalg.solve", a, b)
  a, b = promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))
  # TODO(jakevdp): this condition matches the broadcasting behavior in numpy < 2.0.
  # For the array API specification, we would check only if b.ndim == 1.
  if b.ndim == 1 or a.ndim == b.ndim + 1:
    signature = "(m,m),(m)->(m)"
  else:
    signature = "(m,m),(m,n)->(m,n)"
  return jnp.vectorize(lax_linalg._solve, signature=signature)(a, b)
