@_wraps(scipy.linalg.expm, lax_description=_expm_description)
@partial(jit, static_argnames=('upper_triangular', 'max_squarings'))
def expm(A, *, upper_triangular=False, max_squarings=16):
  P, Q, n_squarings = _calc_P_Q(A)

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
