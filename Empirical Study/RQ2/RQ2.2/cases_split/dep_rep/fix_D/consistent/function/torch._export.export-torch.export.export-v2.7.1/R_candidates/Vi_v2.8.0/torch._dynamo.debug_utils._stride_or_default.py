def _stride_or_default(
    stride: Optional["torch._prims_common.StrideType"],
    *,
    shape: "torch._prims_common.ShapeType",
) -> "torch._prims_common.StrideType":
    return stride if stride is not None else utils.make_contiguous_strides_for(shape)
