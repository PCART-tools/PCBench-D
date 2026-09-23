def _get_ppspec_from_executable(
    executable, mesh
  ) -> tuple[Sequence[ParsedPartitionSpec], Sequence[ParsedPartitionSpec]]:
  input_op_shardings, output_op_sharding = get_op_sharding_from_executable(
      executable
  )
  in_ppspec: list[ParsedPartitionSpec] = []
  for s in input_op_shardings:
    in_ppspec.extend(parse_flatten_op_sharding(s, mesh))

  out_ppspec: list[ParsedPartitionSpec] = []
  for s in output_op_sharding:
    out_ppspec.extend(parse_flatten_op_sharding(s, mesh))
  return in_ppspec, out_ppspec
