def _assertNdSquareness(*arrays):
  for a in arrays:
    m, n = a.shape[-2:]
    if m != n:
      raise np.linalg.LinAlgError(
          'Last 2 dimensions of the array must be square')
