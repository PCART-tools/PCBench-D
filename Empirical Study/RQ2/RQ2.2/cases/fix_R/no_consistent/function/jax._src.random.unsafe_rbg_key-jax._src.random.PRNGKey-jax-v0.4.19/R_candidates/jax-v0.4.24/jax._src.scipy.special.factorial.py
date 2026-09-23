@implements(osp_special.factorial, module='scipy.special')
def factorial(n: ArrayLike, exact: bool = False) -> Array:
  if exact:
    raise NotImplementedError("factorial with exact=True")
  n, = promote_args_inexact("factorial", n)
  return jnp.where(n < 0, 0, lax.exp(lax.lgamma(n + 1)))
