def scalar_mul(xs, a):
  def mul(x):
    dtype = _dtype(x)
    return np.multiply(x, np.array(a, dtype=dtype), dtype=dtype)
  return tree_map(mul, xs)
