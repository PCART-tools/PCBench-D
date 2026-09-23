def find_partitions(jaxpr) -> PartitionInfo:
  (arg_parts, out_parts, num_partitions, local_arg_parts, local_out_parts,
   local_num_partitions) = _find_partitions(jaxpr)

  if local_num_partitions is None:
    local_num_partitions = num_partitions
  if local_arg_parts is None:
    local_arg_parts = arg_parts
  if local_out_parts is None:
    local_out_parts = out_parts

  return PartitionInfo(arg_parts, out_parts, num_partitions,
                       local_arg_parts, local_out_parts, local_num_partitions)
