@register_lowering(aten._scaled_grouped_mm.default, type_promotion_kind=None)
def tuned_scaled_grouped_mm(
    mat_a: TensorBox,
    mat_b: TensorBox,
    scale_a: TensorBox,
    scale_b: TensorBox,
    offs: Optional[TensorBox] = None,
    bias: Optional[TensorBox] = None,
    scale_result: Optional[TensorBox] = None,
    out_dtype: Optional[torch.dtype] = None,
    use_fast_accum: bool = False,
    layout: Optional[Layout] = None,
) -> TensorBox:
    """Auto-tuning for _scaled_grouped_mm() operator."""

    return _tuned_grouped_mm_common(
        "aten._scaled_grouped_mm.default",
        "scaled_grouped_mm",
        aten__scaled_grouped_mm,
        triton_scaled_grouped_mm_template,
        mat_a,
        mat_b,
        scale_a,
        scale_b,
        offs,
        bias,
        scale_result,
        out_dtype,
        use_fast_accum,
        layout,
    )
