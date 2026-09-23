@_wraps(osp_special.expn, module='scipy.special')
@partial(api.custom_jvp, nondiff_argnums=(0,))
@jnp.vectorize
@jit
def expn(n, x):
  n, x = _promote_args_inexact("expn", n, x)
  _c = _lax_const
  zero = _c(x, 0)
  one = _c(x, 1)
  conds = [
    (n < _c(n, 0)) | (x < zero),
    (x == zero) & (n < _c(n, 2)),
    (x == zero) & (n >= _c(n, 2)),
    (n == _c(n, 0)) & (x >= zero),
    (n >= _c(n, 5000)),
    (x > one),
  ]
  n1 = jnp.where(n == _c(n, 1), n + n, n)
  vals = [
    jnp.nan,
    jnp.inf,
    one / n1,  # prevent div by zero
    jnp.exp(-x) / x,
    partial(_expn3, n),
    partial(_expn2, n),
    partial(_expn1, n),
  ]
  ret = jnp.piecewise(x, conds, vals)
  return ret
