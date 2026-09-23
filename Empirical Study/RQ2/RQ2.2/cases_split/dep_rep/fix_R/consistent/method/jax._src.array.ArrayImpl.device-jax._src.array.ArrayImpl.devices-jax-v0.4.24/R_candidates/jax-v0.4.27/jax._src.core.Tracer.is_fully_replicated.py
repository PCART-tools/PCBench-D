  @property
  def is_fully_replicated(self):
    raise ConcretizationTypeError(self,
      f"The is_fully_replicated property was called on {self._error_repr()}."
      f"{self._origin_msg()}")
