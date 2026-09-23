@register_meta(aten._grouped_mm)
@out_wrapper()
def grouped_mm(
    mat_a: Tensor,
    mat_b: Tensor,
    offs: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    out_dtype: Optional[torch.dtype] = None,
) -> Tensor:
    return _meta_grouped_mm_common(
        mat_a,
        mat_b,
        scale_a=None,
        scale_b=None,
        offs=offs,
        bias=bias,
        scale_result=None,
        out_dtype=out_dtype,
    )
