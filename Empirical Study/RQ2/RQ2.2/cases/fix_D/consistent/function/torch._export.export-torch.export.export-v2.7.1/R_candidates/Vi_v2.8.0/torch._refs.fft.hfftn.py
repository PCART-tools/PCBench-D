@register_decomposition(aten.fft_hfftn)
@out_wrapper()
def hfftn(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = None,
    norm: NormType = None,
) -> TensorLikeType:
    shape, dim, last_dim_size = _canonicalize_fft_c2r_shape_and_dim_args(
        "hfftn", input, s, dim
    )
    input = _maybe_promote_tensor_fft(input, require_complex=True)
    input = _resize_fft_input(input, dim, shape)

    tmp = prims.fft_c2c(input, dim=dim[:-1], forward=True) if len(dim) > 1 else input
    tmp = _apply_norm(tmp, norm, _prod(shape[:-1]), forward=True)
    tmp = prims.conj_physical(tmp)
    out = prims.fft_c2r(tmp, dim=dim[-1:], last_dim_size=last_dim_size)
    return _apply_norm(out, norm, last_dim_size, forward=True)
