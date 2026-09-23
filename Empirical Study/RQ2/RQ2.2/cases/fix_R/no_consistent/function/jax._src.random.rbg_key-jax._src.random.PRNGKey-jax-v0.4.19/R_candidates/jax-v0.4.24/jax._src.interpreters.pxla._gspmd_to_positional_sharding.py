def _gspmd_to_positional_sharding(
    out_s: sharding_impls.GSPMDSharding,
    orig_in_s: sharding_impls.PositionalSharding
    ) -> sharding_impls.PositionalSharding:
  return sharding_impls._op_sharding_to_pos_sharding(
      out_s._hlo_sharding, orig_in_s._device_assignment, out_s.memory_kind)
