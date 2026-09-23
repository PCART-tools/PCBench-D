def bcast_iotas_to_reshaped_iota(add, mul, shape, iotas):
  strides = (*map(int, np.cumprod(shape[1:][::-1])[::-1]), 1)
  return reduce(add, [mul(s, i) for i, s in zip(iotas, strides)])  # type: ignore
