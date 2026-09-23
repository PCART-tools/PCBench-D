  def is_compatible_aval(self, aval_shape: Shape):
    assert self._parsed_pspec is not None
    if len(aval_shape) < len(self._parsed_pspec):
      extra_msg = (' For scalars the PartitionSpec should be P()'
                   if len(aval_shape) == 0 else '')
      raise ValueError(
          f"Sharding {self} is only valid for values of rank at least "
          f"{len(self._parsed_pspec)}, but was applied to a value of rank "
          f"{len(aval_shape)}.{extra_msg}")
