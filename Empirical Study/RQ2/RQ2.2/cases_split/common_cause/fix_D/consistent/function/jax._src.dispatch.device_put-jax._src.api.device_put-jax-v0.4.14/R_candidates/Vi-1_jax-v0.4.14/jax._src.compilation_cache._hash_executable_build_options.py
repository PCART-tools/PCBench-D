def _hash_executable_build_options(hash_obj, executable_obj):
  if xla_extension_version > 165:
    expected_options = 11
  else:
    expected_options = 10
  # Ignore private and built-in methods. These can unexpectedly change and lead
  # to false positives, e.g. when different Python versions include different
  # built-ins.
  actual_options = len(
      [x for x in dir(executable_obj) if not x.startswith("_")]
  )
  assert actual_options == expected_options, (
      "Unexpected number of executable_build_options fields: "
      f"{actual_options}, expected: {expected_options}. This likely means "
      "that an extra field was added, and this function needs to be updated."
  )
  if executable_obj.result_layout is not None:
    hash_obj.update(executable_obj.result_layout.to_serialized_proto())
  _hash_int(hash_obj, executable_obj.num_replicas)
  _hash_int(hash_obj, executable_obj.num_partitions)
  _hash_debug_options(hash_obj, executable_obj.debug_options)
  if executable_obj.device_assignment is not None:
    hash_obj.update(executable_obj.device_assignment.serialize())
  _hash_bool(hash_obj, executable_obj.use_spmd_partitioning)
  _hash_bool(hash_obj, executable_obj.use_auto_spmd_partitioning)
  if executable_obj.use_auto_spmd_partitioning:
    if executable_obj.auto_spmd_partitioning_mesh_shape is not None:
      _hash_int_list(hash_obj, executable_obj.auto_spmd_partitioning_mesh_shape)
    if executable_obj.auto_spmd_partitioning_mesh_ids is not None:
      _hash_int_list(hash_obj, executable_obj.auto_spmd_partitioning_mesh_ids)
  _hash_bool_list(
      hash_obj, executable_obj.allow_spmd_sharding_propagation_to_output
  )
  if xla_extension_version > 165 and executable_obj.fdo_profile is not None:
    _hash_string(hash_obj, executable_obj.fdo_profile)
