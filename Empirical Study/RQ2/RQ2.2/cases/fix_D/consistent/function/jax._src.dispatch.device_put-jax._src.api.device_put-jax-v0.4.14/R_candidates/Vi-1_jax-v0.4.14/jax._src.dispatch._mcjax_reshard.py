def _mcjax_reshard(x, target_sharding):
  from jax._src import api, array

  inp_sharding = x.sharding

  if inp_sharding._device_assignment == target_sharding._device_assignment:
    return api.jit(_identity_fn, out_shardings=target_sharding)(x)

  if inp_sharding.device_set != target_sharding.device_set:
    inp_ids = [d.id for d in inp_sharding._device_assignment]
    inp_plat = inp_sharding._device_assignment[0].platform.upper()
    target_ids = [d.id for d in target_sharding._device_assignment]
    target_plat = target_sharding._device_assignment[0].platform.upper()
    raise ValueError("Input and target sharding should have the same set of "
                     f"devices. Got input's device set ids: {inp_ids} on "
                     f"platform {inp_plat} and target sharding's device set "
                     f"ids: {target_ids} on platform {target_plat}")

  old_op_sharding = inp_sharding._to_xla_hlo_sharding(x.ndim).to_proto()
  if op_shardings.is_op_sharding_replicated(old_op_sharding):
    new_op_sharding = old_op_sharding
  else:
    permute_order = np.vectorize(target_sharding._device_assignment.index,
                                 otypes=[int])(inp_sharding._device_assignment)
    new_op_sharding = old_op_sharding.clone()
    new_op_sharding.tile_assignment_devices = np.take(
        old_op_sharding.tile_assignment_devices, permute_order)

  new_x = array.make_array_from_single_device_arrays(
      x.shape,
      GSPMDSharding(target_sharding._device_assignment, new_op_sharding),
      x._arrays)

  _orig_get_and_check_device_assignment = pxla._get_and_check_device_assignment
  pxla._get_and_check_device_assignment = partial(
      _override_get_device_assignment, target_sharding)
  try:
    return api.jit(_identity_fn, out_shardings=target_sharding)(new_x)
  finally:
    pxla._get_and_check_device_assignment = _orig_get_and_check_device_assignment
