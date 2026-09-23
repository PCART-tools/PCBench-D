@register_meta([aten._scaled_grouped_mm.default])
def meta_scaled_grouped_mm(
    mat_a: torch.Tensor,
    mat_b: torch.Tensor,
    scale_a: torch.Tensor,
    scale_b: torch.Tensor,
    offs: Optional[torch.Tensor] = None,
    bias: Optional[torch.Tensor] = None,
    scale_result: Optional[torch.Tensor] = None,
    out_dtype: Optional[torch.dtype] = None,
    use_fast_accum: bool = False,
):
    return _meta_grouped_mm_common(
        mat_a,
        mat_b,
        scale_a=scale_a,
        scale_b=scale_b,
        offs=offs,
        bias=bias,
        scale_result=scale_result,
        out_dtype=out_dtype,
        use_fast_accum=use_fast_accum,
    )
