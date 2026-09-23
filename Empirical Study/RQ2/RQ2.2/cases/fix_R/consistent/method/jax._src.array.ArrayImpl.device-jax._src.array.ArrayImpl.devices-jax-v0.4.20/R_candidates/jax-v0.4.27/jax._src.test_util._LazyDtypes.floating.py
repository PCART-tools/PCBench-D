  @_cached_property
  def floating(self):
    return self.supported([np.float32, np.float64])
