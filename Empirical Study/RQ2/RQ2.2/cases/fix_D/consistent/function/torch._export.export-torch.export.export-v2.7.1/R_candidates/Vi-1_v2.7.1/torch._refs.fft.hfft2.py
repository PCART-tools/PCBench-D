@register_decomposition(aten.fft_hfft2)
@out_wrapper()
def hfft2(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.hfftn(input, s=s, dim=dim, norm=norm)
