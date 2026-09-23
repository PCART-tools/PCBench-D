@register_decomposition(aten.fft_ihfft2)
@out_wrapper()
def ihfft2(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.ihfftn(input, s=s, dim=dim, norm=norm)
