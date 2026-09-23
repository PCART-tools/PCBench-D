@register_decomposition(aten.unfold)
def unfold(
    self: TensorLikeType, dimension: int, size: int, step: int
) -> TensorLikeType:
    shape, strides = _get_unfold_shape_stride(
        self.shape, self.stride(), dimension, size, step
    )
    return self.as_strided(shape, strides)
