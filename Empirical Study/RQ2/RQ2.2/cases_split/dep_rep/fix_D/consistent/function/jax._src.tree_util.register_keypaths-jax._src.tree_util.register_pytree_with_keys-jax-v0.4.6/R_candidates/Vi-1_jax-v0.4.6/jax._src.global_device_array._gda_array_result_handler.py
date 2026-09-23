def _gda_array_result_handler(global_aval, out_sharding, committed,
                              is_out_sharding_from_xla):
  if core.is_opaque_dtype(global_aval.dtype):
    return global_aval.dtype._rules.global_sharded_result_handler(
        global_aval, out_sharding, committed, is_out_sharding_from_xla)
  global_mesh, out_axis_resources = out_sharding.mesh, out_sharding.spec
  global_idx_rid = get_shard_indices_replica_ids(global_aval.shape, global_mesh,
                                                 out_axis_resources)
  local_devices = global_mesh.local_devices
  fast_path_args = _GdaFastPathArgs(global_idx_rid, local_devices)
  return lambda bufs: GlobalDeviceArray(
      global_aval.shape, global_mesh, out_axis_resources, bufs, fast_path_args,
      _enable_checks=False)
