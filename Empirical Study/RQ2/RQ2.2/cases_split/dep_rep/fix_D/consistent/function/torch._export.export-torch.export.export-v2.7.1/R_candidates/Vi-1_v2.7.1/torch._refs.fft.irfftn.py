@register_decomposition(aten.fft_irfftn)
@out_wrapper()
def irfftn(
    input: TensorLikeType,
    s: Optional[ShapeType] = None,
    dim: Optional[DimsType] = None,
    norm: NormType = None,
) -> TensorLikeType:
    shape, dim, last_dim_size = _canonicalize_fft_c2r_shape_and_dim_args(
        "irfftn", input, s, dim
    )
    input = _maybe_promote_tensor_fft(input, require_complex=True)
    input = _resize_fft_input(input, dim, shape)
    out = prims.fft_c2r(input, dim=dim, last_dim_size=last_dim_size)
    return _apply_norm(out, norm, _prod(out.shape[d] for d in dim), forward=False)
