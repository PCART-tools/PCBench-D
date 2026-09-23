  def tobytes(self, order="C"):
    del order
    raise ConcretizationTypeError(self,
      f"The tobytes() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
