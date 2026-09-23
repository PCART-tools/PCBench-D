  @_cached_property
  def complex(self):
    return self.supported([np.complex64, np.complex128])
