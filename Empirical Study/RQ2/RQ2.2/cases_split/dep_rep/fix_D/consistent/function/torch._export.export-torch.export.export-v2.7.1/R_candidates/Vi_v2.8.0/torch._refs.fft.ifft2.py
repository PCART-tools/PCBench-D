@register_decomposition(aten.fft_ifft2)
@out_wrapper()
def ifft2(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.ifftn(input, s=s, dim=dim, norm=norm)
