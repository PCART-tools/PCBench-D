  @_cached_property
  def custom_floats(self):
    return [np.dtype(t) for t in [
      _dtypes.bfloat16, _dtypes.float8_e4m3b11fnuz,
      _dtypes.float8_e4m3fn, _dtypes.float8_e4m3fnuz,
      _dtypes.float8_e5m2, _dtypes.float8_e5m2fnuz]]
