def _assertRankAtLeast2(*arrays):
  for a in arrays:
    if a.ndim < 2:
      raise np.linalg.LinAlgError(
          '%d-dimensional array given. Array must be '
          'at least two-dimensional' % a.ndim)
