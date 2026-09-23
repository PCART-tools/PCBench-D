def array_mapping_to_axis_resources(array_mapping: ArrayMapping):
  if not array_mapping:
    return PartitionSpec()
  max_index = -1
  reverse_map = defaultdict(list)
  for axis, index in array_mapping.items():
    reverse_map[index].append(axis)
    if index > max_index:
      max_index = index
  partitions = tuple(tuple(reverse_map[i]) if reverse_map[i] else None
                     for i in range(max_index + 1))
  return PartitionSpec(*partitions)
