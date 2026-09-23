def op_sharding_to_indices(op_sharding: xc.OpSharding, shape: Sequence[int],
                           num_devices: int) -> Tuple[Tuple[slice, ...], ...]:
  indices = _op_sharding_to_numpy_indices(op_sharding, shape, num_devices)
  return tuple(indices.flat)
