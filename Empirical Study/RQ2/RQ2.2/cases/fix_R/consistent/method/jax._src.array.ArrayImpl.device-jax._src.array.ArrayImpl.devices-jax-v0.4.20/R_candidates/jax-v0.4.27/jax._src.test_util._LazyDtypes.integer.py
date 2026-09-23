  @_cached_property
  def integer(self):
    return self.supported([np.int32, np.int64])
