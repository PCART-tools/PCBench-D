def _inspect_sharding_lowering_rule(ctx: mlir.LoweringRuleContext, value, *,
                                    callback):

  mesh = mesh_lib.thread_resources.env.physical_mesh
  axis_context = ctx.module_context.axis_context

  if isinstance(axis_context, sharding_impls.ShardingContext):
    devices = axis_context.device_assignment
  elif isinstance(axis_context, sharding_impls.SPMDAxisContext):
    devices = list(axis_context.mesh.devices.flat)
  else:
    raise NotImplementedError(type(axis_context))

  # If we have a nontrivial parallel computation, we need to wait until the SPMD
  # partitioner calls back with the `HloSharding.
  def _hlo_sharding_callback(hlo_sharding: xc.HloSharding):
    if mesh.empty:
      return callback(GSPMDSharding(devices, hlo_sharding))
    pspec = parse_flatten_op_sharding(hlo_sharding, mesh)[0].get_partition_spec()
    return callback(NamedSharding(mesh, pspec))

  if len(devices) == 1:
    # If we only have one device in our computation, we can construct a
    # replicated HloSharding and call it right now.
    _hlo_sharding_callback(sharding_impls.get_replicated_hlo_sharding())
    return []

  key = xc.encode_inspect_sharding_callback(_hlo_sharding_callback)
  # We need to make sure `_hlo_sharding_callback` is still alive when the SPMD
  # partitioner runs so we keep it alive by attaching it to the executable.    #
  ctx.module_context.add_keepalive(_hlo_sharding_callback)

  hlo.CustomCallOp([value.type], [value],
                   call_target_name=ir.StringAttr.get(
                     _INSPECT_SHARDING_CALL_NAME),
                   has_side_effect=ir.BoolAttr.get(True),
                   api_version=mlir.i32_attr(1),
                   called_computations=ir.ArrayAttr.get([]),
                   backend_config=ir.StringAttr.get(key),
                   operand_layouts=None,
                   result_layouts=None)
  return []
