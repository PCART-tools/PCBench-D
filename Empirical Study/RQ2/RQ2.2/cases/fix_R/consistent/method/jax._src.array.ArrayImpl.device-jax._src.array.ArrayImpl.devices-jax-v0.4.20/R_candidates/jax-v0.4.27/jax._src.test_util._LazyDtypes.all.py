  @_cached_property
  def all(self):
    return (self.all_floating + self.all_integer + self.all_unsigned +
            self.complex + self.boolean)
