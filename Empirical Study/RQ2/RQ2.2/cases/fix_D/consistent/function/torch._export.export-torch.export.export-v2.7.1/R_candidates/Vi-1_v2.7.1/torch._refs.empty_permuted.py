@out_wrapper()
def empty_permuted(
    shape,
    physical_layout,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[DeviceLikeType] = None,
    requires_grad: bool = False,
    pin_memory: bool = False,
) -> TensorLikeType:
    return prims.empty_permuted(
        shape,
        physical_layout,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
    )
