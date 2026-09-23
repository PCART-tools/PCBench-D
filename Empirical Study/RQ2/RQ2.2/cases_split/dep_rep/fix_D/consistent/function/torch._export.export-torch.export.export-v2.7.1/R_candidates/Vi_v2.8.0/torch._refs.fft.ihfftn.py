@register_decomposition(aten.fft_ihfftn)
@out_wrapper()
def ihfftn(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = None,
    norm: NormType = None,
) -> TensorLikeType:
    torch._check(
        not input.dtype.is_complex,
        lambda: f"ihfftn expects a real-valued input tensor, but got {input.dtype}",
    )
    shape, dim = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    torch._check(len(shape) > 0, lambda: "ihfftn must transform at least one axis")
    input = _maybe_promote_tensor_fft(input, require_complex=False)
    input = _resize_fft_input(input, dim, shape)

    tmp = prims.fft_r2c(input, dim=dim[-1:], onesided=True)

    if len(dim) == 1:
        tmp = _apply_norm(tmp, norm=norm, signal_numel=shape[0], forward=False)
        return prims.conj(tmp)

    tmp = prims.conj_physical(tmp)
    tmp = prims.fft_c2c(tmp, dim=dim[:-1], forward=False)
    return _apply_norm(tmp, norm=norm, signal_numel=_prod(shape), forward=False)
