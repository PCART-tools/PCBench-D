@_wraps(np.linalg.solve)
@jit
def solve(a: ArrayLike, b: ArrayLike) -> Array:
  check_arraylike("jnp.linalg.solve", a, b)
  a, b = promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))
  return lax_linalg._solve(a, b)
