def _sda_sharding(self):
  has_unstacked = any(isinstance(s, Unstacked) for s in self.sharding_spec.sharding)
  if has_unstacked:
    devices = np.array([d.device() for d in self.device_buffers])
    return sharding_internal.PmapSharding(devices, self.sharding_spec)
  raise NotImplementedError(
      'SDAs that are the output of pjit/xmap do not have the sharding attribute '
      'implemented. If you are trying to pass the SDA to pjit/xmap, please '
      'use multihost_utils.host_local_array_to_global_array(...) to convert '
      'SDAs to global `jax.Array` and then pass them to pjit/xmap with '
      '`jax_array` enabled.')
