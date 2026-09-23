def _assertNoEmpty2d(*arrays):
  for a in arrays:
    if _isEmpty2d(a):
      raise np.linalg.LinAlgError("Arrays cannot be empty")
