  def on_device_size_in_bytes(self):
    raise ConcretizationTypeError(self,
      f"The on_device_size_in_bytes() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")
