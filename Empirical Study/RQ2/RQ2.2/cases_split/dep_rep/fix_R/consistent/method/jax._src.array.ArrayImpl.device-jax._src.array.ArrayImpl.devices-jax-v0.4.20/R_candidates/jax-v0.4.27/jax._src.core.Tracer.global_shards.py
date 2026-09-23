  @property
  def global_shards(self):
    raise ConcretizationTypeError(self,
      f"The global_shards property was called on {self._error_repr()}."
      f"{self._origin_msg()}")
