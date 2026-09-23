def to_device(x: TensorBox, device: torch.device, *, copy=False, non_blocking=False):
    device = decode_device(device)
    if x.get_device() == device:
        return clone(x) if copy else x
    return TensorBox.create(ir.DeviceCopy.create(x, device, non_blocking))
