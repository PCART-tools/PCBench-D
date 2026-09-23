@partial(jax.jit, static_argnames=("axis",))
def standardize(x: ArrayLike,
              axis: int | tuple[int, ...] | None = -1,
              mean: ArrayLike | None = None,
              variance: ArrayLike | None = None,
              epsilon: ArrayLike = 1e-5,
              where: ArrayLike | None = None) -> Array:
  r"""Normalizes an array by subtracting ``mean`` and dividing by :math:`\sqrt{\mathrm{variance}}`."""
  numpy_util.check_arraylike("standardize", x)
  numpy_util.check_arraylike_or_none("standardize", mean, variance, where)
  if mean is None:
    mean = jnp.mean(x, axis, keepdims=True, where=where)
  if variance is None:
    # this definition is traditionally seen as less accurate than jnp.var's
    # mean((x - mean(x))**2) but may be faster and even, given typical
    # activation distributions and low-precision arithmetic, more accurate
    # when used in neural network normalization layers
    variance = jnp.mean(
        jnp.square(x), axis, keepdims=True, where=where) - jnp.square(mean)
  return jnp.subtract(x, jnp.asarray(mean)) * lax.rsqrt(jnp.asarray(variance) + epsilon)
