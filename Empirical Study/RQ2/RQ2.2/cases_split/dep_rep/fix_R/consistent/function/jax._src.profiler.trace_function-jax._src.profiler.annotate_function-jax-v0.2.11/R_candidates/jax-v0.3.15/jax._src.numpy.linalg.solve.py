@_wraps(np.linalg.solve)
@jit
def solve(a, b):
  a, b = _promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))
  return lax_linalg._solve(a, b)
