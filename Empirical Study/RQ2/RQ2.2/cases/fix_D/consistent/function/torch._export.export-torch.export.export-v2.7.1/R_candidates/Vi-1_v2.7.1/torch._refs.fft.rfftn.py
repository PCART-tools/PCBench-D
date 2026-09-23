@register_decomposition(aten.fft_rfftn)
@out_wrapper()
def rfftn(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = None,
    norm: NormType = None,
) -> TensorLikeType:
    torch._check(
        not input.dtype.is_complex,
        lambda: f"rfftn expects a real-valued input tensor, but got {input.dtype}",
    )
    shape, dim = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    input = _maybe_promote_tensor_fft(input, require_complex=False)
    input = _resize_fft_input(input, dim, shape)
    out = prims.fft_r2c(input, dim=dim, onesided=True)
    return _apply_norm(out, norm=norm, signal_numel=_prod(shape), forward=True)
