@register_decomposition(aten.fft_fftshift)
def fftshift(input: TensorLikeType, dim: Optional[DimsType] = None) -> TensorLikeType:
    dims = _default_alldims(dim, input)
    shift = [input.shape[d] // 2 for d in dims]
    return torch.roll(input, shift, dims)
