def _device_id_lowering_rule(ctx: LoweringRuleContext):
  return tpu.DeviceIdOp().result
