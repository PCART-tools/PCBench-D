def normalize(x: ArrayLike,
            axis: Optional[Union[int, tuple[int, ...]]] = -1,
            mean: Optional[ArrayLike] = None,
            variance: Optional[ArrayLike] = None,
            epsilon: ArrayLike = 1e-5,
            where: Optional[ArrayLike] = None) -> Array:
  r"""Normalizes an array by subtracting ``mean`` and dividing by :math:`\sqrt{\mathrm{variance}}`."""
  warnings.warn("jax.nn.normalize will be deprecated. Use jax.nn.standardize instead.", DeprecationWarning)
  return standardize(x, axis, mean, variance, epsilon, where)
