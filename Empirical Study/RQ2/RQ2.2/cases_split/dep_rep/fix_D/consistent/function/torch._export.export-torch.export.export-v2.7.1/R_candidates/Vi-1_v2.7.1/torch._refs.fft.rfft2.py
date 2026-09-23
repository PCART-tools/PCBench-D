@register_decomposition(aten.fft_rfft2)
@out_wrapper()
def rfft2(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.rfftn(input, s=s, dim=dim, norm=norm)
