  @_cached_property
  def all_integer(self):
    return self.supported([
        _dtypes.int4, np.int8, np.int16, np.int32, np.int64])
