def weibull_min(key: KeyArrayLike,
                scale: RealArray,
                concentration: RealArray,
                shape: Shape = (),
                dtype: DTypeLikeFloat = float) -> Array:
  r"""Sample from a Weibull distribution.

  The values are distributed according to the probability density function:

  .. math::
     f(x;\sigma,c) \propto x^{c - 1} \exp(-(x / \sigma)^c)

  on the domain :math:`0 < x < \infty`, where :math:`c > 0` is the concentration
  parameter, and :math:`\sigma > 0` is the scale parameter.

  Args:
    key: a PRNG key.
    scale: The scale parameter of the distribution.
    concentration: The concentration parameter of the distribution.
    shape: The shape added to the parameters loc and scale broadcastable shape.
    dtype: The type used for samples.

  Returns:
    A jnp.array of samples.

  """
  key, _ = _check_prng_key("weibull_min", key)
  dtypes.check_user_dtype_supported(dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `weibull_min` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _weibull_min(key, scale, concentration, shape, dtype)
