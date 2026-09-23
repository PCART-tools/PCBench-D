def _get_max_identity(dt):
  return -np.inf if dtypes.issubdtype(dt, np.floating) else np.iinfo(dt).min
