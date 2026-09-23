@register_decomposition(aten.as_strided_scatter)
@out_wrapper()
def as_strided_scatter(
    input: TensorLikeType,
    src: TensorLikeType,
    size: ShapeType,
    stride: StrideType,
    storage_offset: Optional[int] = None,
) -> TensorLikeType:
    storage_offset_int = 0 if storage_offset is None else storage_offset
    return prims.as_strided_scatter(input, src, size, stride, storage_offset_int)
