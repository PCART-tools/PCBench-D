def _gspmd_to_positional_sharding(
    op_sharding: xc.OpSharding,
    self: sharding_impls.PositionalSharding) -> sharding_impls.PositionalSharding:
  return sharding_impls._op_sharding_to_pos_sharding(
      op_sharding, self._device_assignment)
