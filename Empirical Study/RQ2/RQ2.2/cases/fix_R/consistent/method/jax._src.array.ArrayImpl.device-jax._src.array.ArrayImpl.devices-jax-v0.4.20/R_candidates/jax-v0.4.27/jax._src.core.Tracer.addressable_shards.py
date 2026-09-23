  @property
  def addressable_shards(self):
    raise ConcretizationTypeError(self,
      f"The 'addressable_shards' attribute is not available on {self._error_repr()}."
      f"{self._origin_msg()}")
