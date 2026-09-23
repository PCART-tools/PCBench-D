def _inspect_sharding_lowering_rule(ctx: mlir.LoweringRuleContext, value, *,
                                    callback):

  mesh = mesh_lib.thread_resources.env.physical_mesh
  axis_context = ctx.module_context.axis_context

  if isinstance(axis_context, mlir.ShardingContext):
    devices = axis_context.device_assignment
  elif isinstance(axis_context, mlir.SPMDAxisContext):
    devices = list(axis_context.mesh.devices.flat)
  else:
    raise NotImplementedError(type(axis_context))

  def _op_sharding_callback(op_sharding: xc.OpSharding):
    if mesh.empty:
      return callback(GSPMDSharding(
        devices, op_sharding))
    pspec = pjit.parse_flatten_op_sharding(
        op_sharding, mesh)[0].get_partition_spec()
    return callback(NamedSharding(mesh, pspec))

  if len(devices) == 1:
    # If we only have one device in our computation, we can construct a trivial
    # OpSharding and call it right now.
    trivial_sharding = xc.OpSharding()
    trivial_sharding.type = xc.OpSharding.Type.REPLICATED
    _op_sharding_callback(trivial_sharding)
    return []

  # If we have a nontrivial parallel computation, we need to wait until the SPMD
  # partitioner calls back with the `HloSharding.
  def _hlo_sharding_callback(hlo_sharding):
    op_sharding = hlo_sharding.to_proto()
    return _op_sharding_callback(op_sharding)

  # Here we store information in a container that we store globally so the
  # custom partitioning code can access it.
  sharding_callback_info = ShardingCallbackInfo(_hlo_sharding_callback,
                                                ctx.module_context)
  key = str(id(sharding_callback_info))
  sharding_callbacks[key] = sharding_callback_info
  # We need to make sure `sharding_callback_info` is still alive when the SPMD
  # partitioner runs so we keep it alive by attaching it to the executable.
  ctx.module_context.add_keepalive(sharding_callback_info)

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
