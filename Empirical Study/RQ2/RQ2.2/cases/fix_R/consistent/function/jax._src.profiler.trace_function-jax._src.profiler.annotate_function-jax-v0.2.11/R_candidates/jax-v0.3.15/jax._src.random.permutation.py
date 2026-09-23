def permutation(key: KeyArray,
                x: Union[int, Array],
                axis: int = 0,
                independent: bool = False) -> jnp.ndarray:
  """Returns a randomly permuted array or range.

  Args:
    key: a PRNG key used as the random key.
    x: int or array. If x is an integer, randomly shuffle np.arange(x).
      If x is an array, randomly shuffle its elements.
    axis: int, optional. The axis which x is shuffled along. Default is 0.
    independent: bool, optional. If set to True, each individual vector along
      the given axis is shuffled independently. Default is False.

  Returns:
    A shuffled version of x or array range
  """
  key, _ = _check_prng_key(key)
  _check_arraylike("permutation", x)
  axis = canonicalize_axis(axis, np.ndim(x) or 1)
  if not np.ndim(x):
    if not np.issubdtype(lax.dtype(x), np.integer):
      raise TypeError("x must be an integer or at least 1-dimensional")
    r = core.concrete_or_error(int, x, 'argument x of jax.random.permutation()')
    return _shuffle(key, jnp.arange(r), axis)
  if independent or np.ndim(x) == 1:
    return _shuffle(key, x, axis)
  ind = _shuffle(key, jnp.arange(x.shape[axis]), 0)  # type: ignore[union-attr]
  return jnp.take(x, ind, axis)
