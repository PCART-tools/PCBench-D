@register_decomposition(aten.fft_fft2)
@out_wrapper()
def fft2(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.fftn(input, s=s, dim=dim, norm=norm)
