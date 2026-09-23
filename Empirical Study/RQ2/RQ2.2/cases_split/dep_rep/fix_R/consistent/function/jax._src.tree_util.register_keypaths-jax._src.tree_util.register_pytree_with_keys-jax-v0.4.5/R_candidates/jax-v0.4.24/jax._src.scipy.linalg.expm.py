@implements(scipy.linalg.expm, lax_description=_expm_description)
@partial(jit, static_argnames=('upper_triangular', 'max_squarings'))
def expm(A: ArrayLike, *, upper_triangular: bool = False, max_squarings: int = 16) -> Array:
  A, = promote_dtypes_inexact(A)

  if A.ndim < 2 or A.shape[-1] != A.shape[-2]:
    raise ValueError(f"Expected A to be a (batched) square matrix, got {A.shape=}.")

  if A.ndim > 2:
    return jnp.vectorize(
      partial(expm, upper_triangular=upper_triangular, max_squarings=max_squarings),
      signature="(n,n)->(n,n)")(A)

  P, Q, n_squarings = _calc_P_Q(jnp.asarray(A))

  def _nan(args):
    A, *_ = args
    return jnp.full_like(A, jnp.nan)

  def _compute(args):
    A, P, Q = args
    R = _solve_P_Q(P, Q, upper_triangular)
    R = _squaring(R, n_squarings, max_squarings)
    return R

  R = lax.cond(n_squarings > max_squarings, _nan, _compute, (A, P, Q))
  return R
