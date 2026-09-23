def _get_partition_spec(ppspec: Sequence[ParsedPartitionSpec]) -> Sequence[PartitionSpec]:
  return [_get_single_pspec(p) for p in ppspec]
