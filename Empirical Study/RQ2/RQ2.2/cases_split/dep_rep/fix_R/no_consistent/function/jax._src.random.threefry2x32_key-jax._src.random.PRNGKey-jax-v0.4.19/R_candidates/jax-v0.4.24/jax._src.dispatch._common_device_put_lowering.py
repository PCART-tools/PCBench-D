def _common_device_put_lowering(ctx, x, *, device, src):
  if (isinstance(device, (XLACompatibleSharding, TransferToMemoryKind)) and
      device.memory_kind is not None):
    raise NotImplementedError(
        "Passing memory_kind to device_put via Shardings is not supported on"
        f" platforms {ctx.module_context.platforms}")
  return [x]
