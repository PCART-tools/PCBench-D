class _PmapFastpathData(NamedTuple):
  version: int  # For forward and backward compatibility
  xla_executable: xc.LoadedExecutable
  in_handler: Any
  out_handler: Any
  out_pytree_def: Any
  # Data needed to handle the inputs.
  input_devices: Sequence[xc.Device]
  input_indices: Sequence[sharding_specs.Index]
  input_array_shardings: Sequence[Any]
  # Data needed to build the Array from C++.
  out_avals: Sequence[Any]
  out_array_shardings: Sequence[Any]
  out_committed: Sequence[Any]
