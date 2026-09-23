  @property
  def is_fully_addressable(self):
    raise ConcretizationTypeError(self,
      f"The is_fully_addressable property was called on {self._error_repr()}."
      f"{self._origin_msg()}")
