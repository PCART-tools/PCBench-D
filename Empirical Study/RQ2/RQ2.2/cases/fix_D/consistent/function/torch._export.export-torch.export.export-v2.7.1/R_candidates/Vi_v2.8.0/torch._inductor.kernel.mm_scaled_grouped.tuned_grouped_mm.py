@register_lowering(aten._grouped_mm.default, type_promotion_kind=None)
def tuned_grouped_mm(
    mat_a: TensorBox,
    mat_b: TensorBox,
    offs: Optional[TensorBox] = None,
    bias: Optional[TensorBox] = None,
    out_dtype: Optional[torch.dtype] = None,
    layout: Optional[Layout] = None,
) -> TensorBox:
    """Auto-tuning for _grouped_mm() operator."""

    return _tuned_grouped_mm_common(
        "aten._grouped_mm.default",
        "grouped_mm",
        aten__grouped_mm,
        triton_grouped_mm_template,
        mat_a,
        mat_b,
        None,
        None,
        offs,
        bias,
        None,
        out_dtype,
        None,
        layout,
    )
