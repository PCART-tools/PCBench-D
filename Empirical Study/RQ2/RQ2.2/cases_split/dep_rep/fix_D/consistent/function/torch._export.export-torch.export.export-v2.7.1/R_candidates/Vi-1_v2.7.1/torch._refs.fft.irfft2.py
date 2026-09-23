@register_decomposition(aten.fft_irfft2)
@out_wrapper()
def irfft2(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.irfftn(input, s=s, dim=dim, norm=norm)
