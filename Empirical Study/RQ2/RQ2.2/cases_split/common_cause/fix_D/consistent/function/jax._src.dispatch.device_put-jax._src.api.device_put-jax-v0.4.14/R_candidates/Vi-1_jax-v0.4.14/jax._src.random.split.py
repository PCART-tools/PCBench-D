def split(key: KeyArray, num: Union[int, tuple[int, ...]] = 2) -> KeyArray:
  """Splits a PRNG key into `num` new keys by adding a leading axis.

  Args:
    key: a PRNG key (from ``PRNGKey``, ``split``, ``fold_in``).
    num: optional, a positive integer (or tuple of integers) indicating
      the number (or shape) of keys to produce. Defaults to 2.

  Returns:
    An array-like object of `num` new PRNG keys.
  """
  key, wrapped = _check_prng_key(key)
  return _return_prng_keys(wrapped, _split(key, num))
