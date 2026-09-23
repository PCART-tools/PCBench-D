def numpy_vecdot(x, y, axis):
  """Implementation of numpy.vecdot for testing on numpy < 2.0.0"""
  if numpy_version() >= (2, 0, 0):
    raise ValueError("should be calling vecdot directly on numpy 2.0.0")
  x = np.moveaxis(x, axis, -1)
  y = np.moveaxis(y, axis, -1)
  x, y = np.broadcast_arrays(x, y)
  return np.matmul(np.conj(x[..., None, :]), y[..., None])[..., 0, 0]
