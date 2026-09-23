def _device_put_lowering(ctx, x, *, device, src):
  if (isinstance(device, (XLACompatibleSharding, TransferToMemoryKind)) and
      device.memory_kind is not None):
    aval, = ctx.avals_in
    out_aval, = ctx.avals_out
    x = mlir.wrap_with_memory_kind(x, device.memory_kind, out_aval)
    if isinstance(device, XLACompatibleSharding):
      x = mlir.wrap_with_sharding_op(
          ctx, x, out_aval, device._to_xla_hlo_sharding(aval.ndim).to_proto())
    return [x]
  return [x]
