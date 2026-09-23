def rand_int(rng, low=0, high=None):
  def fn(shape, dtype):
    nonlocal high
    if low == 0 and high is None:
      if np.issubdtype(dtype, np.integer):
        high = np.iinfo(dtype).max
      else:
        raise ValueError("rand_int requires an explicit `high` value for "
                         "non-integer types.")
    return rng.randint(low, high=high, size=shape, dtype=dtype)
  return fn
