def _check_in_pmap_sharding_with_arrays(args, in_axes_flat, in_devices):
  from jax.experimental import sharding

  if not args:
    return

  if in_devices is not None:
    in_devices = np.array(in_devices)

  first_arr_devices = args[0].sharding.devices
  for a, i in safe_zip(args, in_axes_flat):
    assert isinstance(a.sharding, sharding.PmapSharding)
    arr_sharding = a.sharding.sharded_dim
    arr_devices = a.sharding.devices
    if arr_sharding != i:
      raise ValueError('Array and pmap sharding does not match. Got pmap '
                       f'sharding: {i}, Array sharding: {arr_sharding} for '
                       f'arg: {a}')
    if (in_devices is not None and
        arr_devices is not None and
        not np.array_equal(arr_devices, in_devices)):
      raise ValueError('Devices passed to pmap and Array should be equal. '
                       f'Got pmap devices: {devices}, Array devices: '
                       f'{arr_devices} for arg: {a}')
    if (in_devices is None and
        not np.array_equal(arr_devices, first_arr_devices)):
      raise ValueError('Devices of all `Array` inputs should be the same. '
                       f'Got array device: {arr_devices}, '
                       f'another array device: {first_arr_devices}')
  return first_arr_devices
