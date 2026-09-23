def _op_sharding_to_pos_sharding(
    op_sharding: xc.OpSharding | xc.HloSharding,
    device_assignment: Sequence[xc.Device]) -> PositionalSharding:
  if isinstance(op_sharding, xc.HloSharding):
    op_sharding = op_sharding.to_proto()  # type: ignore

  if op_sharding.type == xc.OpSharding.Type.REPLICATED:
    return PositionalSharding(device_assignment).replicate()

  if op_sharding.last_tile_dims == [xc.OpSharding.Type.REPLICATED]:
    replicate_on_last_tile_dim = True
  else:
    replicate_on_last_tile_dim = op_sharding.replicate_on_last_tile_dim
    if op_sharding.last_tile_dims:
      raise NotImplementedError(
          "Unhandled OpSharding type. Please open a bug report!")

  name = device_assignment[0].platform.upper()
  ids = np.array([DeviceIdSet(name, i)
                  for i in op_sharding.tile_assignment_devices])
  p = PositionalSharding._remake(tuple(device_assignment), ids)
  p = p.reshape(op_sharding.tile_assignment_dimensions)
  if replicate_on_last_tile_dim:
    p = p.replicate(-1, keepdims=False)
  return p
