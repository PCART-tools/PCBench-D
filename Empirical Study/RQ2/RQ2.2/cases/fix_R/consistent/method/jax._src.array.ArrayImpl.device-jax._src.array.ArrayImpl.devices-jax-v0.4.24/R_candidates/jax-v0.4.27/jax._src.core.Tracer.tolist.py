  def tolist(self):
    raise ConcretizationTypeError(self,
      f"The tolist() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
