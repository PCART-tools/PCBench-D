@register_noop_decomp(torch.ops.prims.device_put)
def device_put_noop(x, device, non_blocking=True):
    return x.device == decode_device(device)
