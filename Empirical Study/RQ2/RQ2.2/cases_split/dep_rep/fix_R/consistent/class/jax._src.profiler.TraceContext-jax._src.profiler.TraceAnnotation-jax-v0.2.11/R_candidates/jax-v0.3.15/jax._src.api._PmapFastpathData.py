class _PmapFastpathData(NamedTuple):
  version: int  # For forward and backward compatibility
  xla_executable: xla.XlaExecutable
  in_handler: Any
  out_handler: Any
  out_pytree_def: Any
  # Data needed to handle the inputs.
  input_sharding_specs: Sequence[pxla.ShardingSpec]
  input_devices: Sequence[xc.Device]
  input_indices: Sequence[pxla.Index]
  # Data needed to build the ShardedDeviceArray from C++.
  out_sharding_specs: Sequence[pxla.ShardingSpec]
  out_indices: Sequence[pxla.Index]
  out_avals: Sequence[Any]
