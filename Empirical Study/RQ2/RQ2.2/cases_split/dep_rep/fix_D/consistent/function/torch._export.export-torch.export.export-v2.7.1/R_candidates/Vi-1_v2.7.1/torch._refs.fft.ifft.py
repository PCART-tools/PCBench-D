@register_decomposition(aten.fft_ifft)
@out_wrapper()
def ifft(
    input: TensorLikeType,
    n: Optional[int] = None,
    dim: int = -1,
    norm: NormType = None,
) -> TensorLikeType:
    if input.dtype.is_complex:
        return _fft_c2c("ifft", input, n, dim, norm, forward=False)
    else:
        return _fft_r2c("ifft", input, n, dim, norm, forward=False, onesided=False)
