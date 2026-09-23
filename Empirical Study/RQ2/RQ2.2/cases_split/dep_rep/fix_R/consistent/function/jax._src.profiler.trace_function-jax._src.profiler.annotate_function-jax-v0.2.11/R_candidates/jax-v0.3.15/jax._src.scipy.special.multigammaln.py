@_wraps(osp_special.multigammaln, update_doc=False)
def multigammaln(a, d):
  d = core.concrete_or_error(int, d, "d argument of multigammaln")
  a, d_ = _promote_args_inexact("multigammaln", a, d)

  constant = lax.mul(lax.mul(lax.mul(_lax_const(a, 0.25), d_),
                             lax.sub(d_, _lax_const(a, 1))),
                     lax.log(_lax_const(a, np.pi)))
  b = lax.div(jnp.arange(d, dtype=d_.dtype), _lax_const(a, 2))
  res = jnp.sum(gammaln(jnp.expand_dims(a, axis=-1) -
                        jnp.expand_dims(b, axis=tuple(range(a.ndim)))),
                axis=-1)
  return res + constant
