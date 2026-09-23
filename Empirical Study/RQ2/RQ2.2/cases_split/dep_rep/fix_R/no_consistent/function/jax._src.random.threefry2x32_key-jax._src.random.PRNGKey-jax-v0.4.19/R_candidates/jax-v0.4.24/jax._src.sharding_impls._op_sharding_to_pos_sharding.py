def _op_sharding_to_pos_sharding(
    op_sharding: xc.OpSharding | xc.HloSharding,
    device_assignment: Sequence[xc.Device],
    memory_kind: str | None = None) -> PositionalSharding:
  if isinstance(op_sharding, xc.OpSharding):
    op_sharding = xc.HloSharding.from_proto(op_sharding)  # type: ignore

  if op_sharding.is_replicated():
    return PositionalSharding(
        device_assignment, memory_kind=memory_kind).replicate()

  if len(op_sharding.subgroup_types()) > 1:
    raise NotImplementedError(
        'Unhandled HloSharding type. Please open a bug report!'
    )

  name = device_assignment[0].platform.upper()
  ids = np.array(
      [DeviceIdSet(name, i) for i in op_sharding.tile_assignment_devices()]
  )
  p = PositionalSharding._remake(tuple(device_assignment), ids,
                                 memory_kind=memory_kind)
  p = p.reshape(op_sharding.tile_assignment_dimensions())
  if op_sharding.replicate_on_last_tile_dim():
    p = p.replicate(-1, keepdims=False)
  return p
