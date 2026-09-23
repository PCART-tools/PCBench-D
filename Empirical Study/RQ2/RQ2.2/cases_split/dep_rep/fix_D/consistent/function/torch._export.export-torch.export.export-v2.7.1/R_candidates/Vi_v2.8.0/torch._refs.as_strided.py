def as_strided(
    a: TensorLikeType,
    size: ShapeType,
    stride: StrideType,
    storage_offset: Optional[int] = None,
) -> TensorLikeType:
    storage_offset_int = (
        storage_offset if storage_offset is not None else a.storage_offset()
    )
    return prims.as_strided(a, size, stride, storage_offset_int)
