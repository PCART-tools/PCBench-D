def rand_unique_int(rng, high=None):
  def fn(shape, dtype):
    return rng.choice(np.arange(high or prod(shape), dtype=dtype),
                      size=shape, replace=False)
  return fn
