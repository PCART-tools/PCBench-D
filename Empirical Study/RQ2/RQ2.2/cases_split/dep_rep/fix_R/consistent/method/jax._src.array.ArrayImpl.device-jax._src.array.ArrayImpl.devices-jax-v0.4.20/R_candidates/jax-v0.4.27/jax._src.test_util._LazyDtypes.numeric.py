  @_cached_property
  def numeric(self):
    return self.floating + self.integer + self.unsigned + self.complex
