@_wraps(osp_special.gamma, module='scipy.special', lax_description="""\
The JAX version only accepts real-valued inputs.""")
def gamma(x: ArrayLike) -> Array:
  x, = promote_args_inexact("gamma", x)
  return lax.exp(lax.lgamma(x))
