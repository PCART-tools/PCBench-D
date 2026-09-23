  def delete(self):
    raise ConcretizationTypeError(self,
      f"The delete() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
