@implements(osp_special.gamma, module='scipy.special', lax_description="""\
The JAX version only accepts real-valued inputs.""")
def gamma(x: ArrayLike) -> Array:
  x, = promote_args_inexact("gamma", x)
  # Compute the sign for negative x, matching the semantics of scipy.special.gamma
  floor_x = lax.floor(x)
  sign = jnp.where((x > 0) | (x == floor_x), 1.0, (-1.0) ** floor_x)
  return sign * lax.exp(lax.lgamma(x))
