  def devices(self):
    raise ConcretizationTypeError(self,
      f"The devices() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
