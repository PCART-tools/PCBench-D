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

  old_hlo_sharding = inp_sharding._to_xla_hlo_sharding(x.ndim)
  if old_hlo_sharding.is_replicated():
    new_hlo_sharding = old_hlo_sharding
  else:
    permute_order = np.vectorize(target_sharding._device_assignment.index,
                                 otypes=[int])(inp_sharding._device_assignment)
    # Unfortunately need to fallback to V1 sharding here.
    new_op_sharding = old_hlo_sharding.to_proto()
    new_op_sharding.iota_reshape_dims = []
    new_op_sharding.iota_transpose_perm = []
    new_op_sharding.tile_assignment_devices = np.take(
        old_hlo_sharding.tile_assignment_devices(), permute_order
    )
    new_hlo_sharding = xc.HloSharding.from_proto(new_op_sharding)

  new_x = array.make_array_from_single_device_arrays(
      x.shape,
      GSPMDSharding(target_sharding._device_assignment, new_hlo_sharding),
      x._arrays,
  )

  _orig_get_and_check_device_assignment = pxla._get_and_check_device_assignment.fn
  pxla._get_and_check_device_assignment.fn = partial(
      _override_get_device_assignment, target_sharding)
  try:
    return api.jit(_identity_fn, out_shardings=target_sharding)(new_x)
  finally:
    pxla._get_and_check_device_assignment.fn = _orig_get_and_check_device_assignment
