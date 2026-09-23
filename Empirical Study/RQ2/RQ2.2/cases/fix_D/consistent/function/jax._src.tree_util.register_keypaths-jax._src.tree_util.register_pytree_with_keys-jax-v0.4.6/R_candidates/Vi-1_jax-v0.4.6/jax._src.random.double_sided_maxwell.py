def double_sided_maxwell(key: KeyArray,
                         loc: RealArray,
                         scale: RealArray,
                         shape: Shape = (),
                         dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  """Sample from a double sided Maxwell distribution.

  Samples using:
     loc + scale* sgn(U-0.5)* one_sided_maxwell U~Unif;

  Args:
    key: a PRNG key.
    loc: The location parameter of the distribution.
    scale: The scale parameter of the distribution.
    shape: The shape added to the parameters loc and scale broadcastable shape.
    dtype: The type used for samples.

  Returns:
    A jnp.array of samples.

  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `double_sided_maxwell` must be a float"
                     f" dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _double_sided_maxwell(key, loc, scale, shape, dtype)
