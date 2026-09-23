def _get_min_identity(dt):
  return np.inf if dtypes.issubdtype(dt, np.floating) else np.iinfo(dt).max
