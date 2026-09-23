  def unsafe_buffer_pointer(self):
    raise ConcretizationTypeError(self,
      f"The unsafe_buffer_pointer() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
