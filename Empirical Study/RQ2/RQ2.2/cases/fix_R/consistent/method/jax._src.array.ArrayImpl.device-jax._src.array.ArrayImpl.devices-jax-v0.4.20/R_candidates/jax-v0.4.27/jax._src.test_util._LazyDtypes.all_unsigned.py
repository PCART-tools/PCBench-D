  @_cached_property
  def all_unsigned(self):
    return self.supported([
        _dtypes.uint4, np.uint8, np.uint16, np.uint32, np.uint64])
