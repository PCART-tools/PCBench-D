@register_decomposition([aten.arange.start])
def arange_start(
    start: NumberType,
    end: NumberType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    pin_memory: bool = False,
):
    return aten.arange.start_step(
        start, end, 1, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )
