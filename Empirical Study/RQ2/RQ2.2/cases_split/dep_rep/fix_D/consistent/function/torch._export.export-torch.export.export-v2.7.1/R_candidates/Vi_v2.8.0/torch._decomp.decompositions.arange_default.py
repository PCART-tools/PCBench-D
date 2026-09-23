@register_decomposition([aten.arange.default, aten.arange.out])
@out_wrapper()
def arange_default(
    end: NumberType,
    *,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    pin_memory: bool = False,
):
    return aten.arange.start_step(
        0, end, 1, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )
