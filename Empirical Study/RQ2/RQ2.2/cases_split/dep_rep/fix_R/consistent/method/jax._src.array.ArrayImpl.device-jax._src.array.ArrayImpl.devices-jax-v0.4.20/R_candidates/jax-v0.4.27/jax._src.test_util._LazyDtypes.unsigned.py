  @_cached_property
  def unsigned(self):
    return self.supported([np.uint32, np.uint64])
