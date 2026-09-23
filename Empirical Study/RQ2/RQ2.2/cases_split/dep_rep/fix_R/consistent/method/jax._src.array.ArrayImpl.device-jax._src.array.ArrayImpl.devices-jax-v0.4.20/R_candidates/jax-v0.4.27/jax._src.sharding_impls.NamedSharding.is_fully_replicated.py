  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    if self.mesh.size == 1:
      return True
    array_mapping = cast(ParsedPartitionSpec, get_array_mapping(self._parsed_pspec))
    mesh_shape = self.mesh.shape
    num_partitions = 1
    for name in array_mapping:
      num_partitions *= mesh_shape[name]
    return num_partitions == 1
