def rademacher(key: KeyArray,
               shape: Shape,
               dtype: DTypeLikeInt = dtypes.int_) -> Array:
  r"""Sample from a Rademacher distribution.

  The values are distributed according to the probability mass function:

  .. math::
     f(k) = \frac{1}{2}(\delta(k - 1) + \delta(k + 1))

  on the domain :math:`k \in \{-1, 1}`, where `\delta(x)` is the dirac delta function.

  Args:
    key: a PRNG key.
    shape: The shape of the returned samples.
    dtype: The type used for samples.

  Returns:
    A jnp.array of samples, of shape `shape`. Each element in the output has
    a 50% change of being 1 or -1.

  """
  key, _ = _check_prng_key(key)
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _rademacher(key, shape, dtype)
