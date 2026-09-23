def round(x):
  return np.trunc(
    x + np.copysign(np.nextafter(np.array(.5, dtype=x.dtype),
                                 np.array(0., dtype=x.dtype),
                                 dtype=x.dtype), x)).astype(x.dtype)
