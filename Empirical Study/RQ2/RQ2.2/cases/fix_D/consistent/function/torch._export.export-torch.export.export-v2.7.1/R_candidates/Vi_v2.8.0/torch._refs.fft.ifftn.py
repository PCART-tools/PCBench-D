@register_decomposition(aten.fft_ifftn)
@out_wrapper()
def ifftn(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = None,
    norm: NormType = None,
) -> TensorLikeType:
    (shape, dim) = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    x = _maybe_promote_tensor_fft(input, require_complex=True)
    return _fftn_c2c("ifftn", x, shape, dim, norm, forward=False)
