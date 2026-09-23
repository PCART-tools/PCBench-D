  def addressable_data(self, index):
    raise ConcretizationTypeError(self,
      f"The addressable_data() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
