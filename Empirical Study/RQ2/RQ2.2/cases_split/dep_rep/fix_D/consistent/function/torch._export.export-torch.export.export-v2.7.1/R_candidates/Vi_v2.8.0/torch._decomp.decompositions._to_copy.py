@register_decomposition(aten._to_copy)
@out_wrapper()
def _to_copy(
    x: Union[Tensor, NumberType],
    *,
    dtype: Optional[torch.dtype] = None,
    layout=None,
    device: Optional[torch.device] = None,
    pin_memory: bool = False,
    non_blocking: bool = False,
    memory_format: Optional[torch.memory_format] = None,
):
    assert not layout or layout == torch.strided, "TODO"
    assert not pin_memory, "TODO"
    assert isinstance(x, (torch.Tensor, int, float, bool, complex))
    if device is None and dtype is None and memory_format is None:
        if isinstance(x, torch.Tensor):
            return x.clone()
        else:
            return x
    dtype_converted = False

    if isinstance(x, torch.Tensor):
        x_tensor = x
    else:
        x_tensor = torch.scalar_tensor(x)

    if device is not None and device != x_tensor.device:
        # avoid conversions on cpu
        if dtype is not None and device.type == "cpu":
            x_tensor = torch._prims.convert_element_type(x_tensor, dtype)
            dtype_converted = True
        x_tensor = torch._prims.device_put(x_tensor, device, non_blocking)

    if dtype is not None and not dtype_converted:
        x_tensor = torch._prims.convert_element_type(x_tensor, dtype)
        dtype_converted = True

    if memory_format is not None:  # no ref/prim for memory format
        return torch.clone(x_tensor, memory_format=memory_format)
    return x_tensor
