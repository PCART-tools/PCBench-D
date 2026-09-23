def _get_ppspec_from_executable(executable, mesh) -> Tuple[Sequence[ParsedPartitionSpec], Sequence[ParsedPartitionSpec]]:
  input_op_shardings: Sequence[xc.OpSharding] = executable.hlo_modules()[0].spmd_parameters_shardings
  output_op_sharding: xc.OpSharding = executable.hlo_modules()[0].spmd_output_sharding
  in_ppspec: List[ParsedPartitionSpec] = []
  for s in input_op_shardings:
    in_ppspec.extend(parse_flatten_op_sharding(s, mesh))
  out_ppspec = parse_flatten_op_sharding(output_op_sharding, mesh)
  return in_ppspec, out_ppspec
