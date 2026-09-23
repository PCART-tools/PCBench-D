@custom_derivatives.custom_jvp
@implements(osp_special.poch, module='scipy.special', lax_description="""\
The JAX version only accepts positive and real inputs.""")
def poch(z: ArrayLike, m: ArrayLike) -> Array:
  # Factorial definition when m is close to an integer, otherwise gamma definition.
  z, m = promote_args_inexact("poch", z, m)

  return jnp.where(m == 0., jnp.array(1, dtype=z.dtype), gamma(z + m) / gamma(z))
