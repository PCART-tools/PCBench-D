def fold_in(key: KeyArray, data: IntegerArray) -> KeyArray:
  """Folds in data to a PRNG key to form a new PRNG key.

  Args:
    key: a PRNG key (from ``PRNGKey``, ``split``, ``fold_in``).
    data: a 32bit integer representing data to be folded in to the key.

  Returns:
    A new PRNG key that is a deterministic function of the inputs and is
    statistically safe for producing a stream of new pseudo-random values.
  """
  key, wrapped = _check_prng_key(key)
  return _return_prng_keys(wrapped, _fold_in(key, data))
