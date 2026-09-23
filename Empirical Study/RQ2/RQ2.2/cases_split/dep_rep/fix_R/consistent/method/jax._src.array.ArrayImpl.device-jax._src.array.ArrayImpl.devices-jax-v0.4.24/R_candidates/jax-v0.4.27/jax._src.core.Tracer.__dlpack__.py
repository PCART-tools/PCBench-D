  def __dlpack__(self, *args, **kw):
    raise ConcretizationTypeError(self,
      f"The __dlpack__() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
