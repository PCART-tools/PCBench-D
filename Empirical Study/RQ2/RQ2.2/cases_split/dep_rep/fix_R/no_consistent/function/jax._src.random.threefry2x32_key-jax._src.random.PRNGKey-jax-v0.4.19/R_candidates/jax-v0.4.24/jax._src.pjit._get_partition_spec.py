def _get_partition_spec(
    ppspec: Sequence[ParsedPartitionSpec]) -> Sequence[PartitionSpec]:
  return [get_single_pspec(p) for p in ppspec]
