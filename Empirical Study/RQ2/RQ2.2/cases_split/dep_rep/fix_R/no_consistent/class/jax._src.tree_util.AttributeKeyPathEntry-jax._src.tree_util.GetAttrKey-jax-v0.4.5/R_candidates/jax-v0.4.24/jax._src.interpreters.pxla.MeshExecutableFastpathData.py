class MeshExecutableFastpathData(NamedTuple):
  xla_executable: xc.LoadedExecutable
  out_pytree_def: Any
  in_shardings: Sequence[sharding_impls.XLACompatibleSharding]
  out_shardings: Sequence[sharding_impls.XLACompatibleSharding]
  out_avals: Sequence[ShapedArray]
  out_committed: Sequence[bool]
  kept_var_bitvec: Iterable[bool]
  # TODO(yashkatariya): Remove once minimum jaxlib version is 0.4.24
  arg_handler_devices: Sequence[xc.Device]
  arg_handler_indices: Sequence[tuple[Index | None, ...]]
