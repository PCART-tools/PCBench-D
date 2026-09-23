@implements(osp_special.bernoulli, module='scipy.special')
def bernoulli(n: int) -> Array:
  # Generate Bernoulli numbers using the Chowla and Hartung algorithm.
  n = core.concrete_or_error(operator.index, n, "Argument n of bernoulli")
  if n < 0:
    raise ValueError("n must be a non-negative integer.")
  b3 = jnp.array([1, -1/2, 1/6])
  if n < 3:
    return b3[:n + 1]
  bn = jnp.zeros(n + 1).at[:3].set(b3)
  m = jnp.arange(4, n + 1, 2, dtype=bn.dtype)
  q1 = (1. / jnp.pi ** 2) * jnp.cumprod(-(m - 1) * m / 4 / jnp.pi ** 2)
  k = jnp.arange(2, 50, dtype=bn.dtype)  # Choose 50 because 2 ** -50 < 1E-15
  q2 = jnp.sum(k[:, None] ** -m[None, :], axis=0)
  return bn.at[4::2].set(q1 * (1 + q2))
