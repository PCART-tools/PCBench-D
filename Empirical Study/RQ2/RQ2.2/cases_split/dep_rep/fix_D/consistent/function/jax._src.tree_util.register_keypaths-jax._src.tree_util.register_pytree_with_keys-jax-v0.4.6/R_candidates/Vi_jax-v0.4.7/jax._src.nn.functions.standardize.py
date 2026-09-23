@partial(jax.jit, static_argnames=("axis",))
def standardize(x: Array,
              axis: Optional[Union[int, Tuple[int, ...]]] = -1,
              mean: Optional[Array] = None,
              variance: Optional[Array] = None,
              epsilon: Array = 1e-5,
              where: Optional[Array] = None) -> Array:
  r"""Normalizes an array by subtracting ``mean`` and dividing by :math:`\sqrt{\mathrm{variance}}`."""
  if mean is None:
    mean = jnp.mean(x, axis, keepdims=True, where=where)
  if variance is None:
    # this definition is traditionally seen as less accurate than jnp.var's
    # mean((x - mean(x))**2) but may be faster and even, given typical
    # activation distributions and low-precision arithmetic, more accurate
    # when used in neural network normalization layers
    variance = jnp.mean(
        jnp.square(x), axis, keepdims=True, where=where) - jnp.square(mean)
  return (x - mean) * lax.rsqrt(variance + epsilon)
