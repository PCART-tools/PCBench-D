def _axis_index_rule(ctx: LoweringRuleContext, *, axis_name: str):
  device_id = _make_index(tpu.DeviceIdOp().result)
  l_to_m = ctx.lowering_context.mesh_context.logical_to_mesh
  axis_names = ctx.lowering_context.mesh_context.axis_names
  col = _make_index(axis_names.index(axis_name))
  return memref.LoadOp(l_to_m, [device_id, col]).result
