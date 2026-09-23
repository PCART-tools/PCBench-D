def is_contiguous_strides_for_shape(
    stride: Sequence[_IntLike], shape: Sequence[_IntLike]
) -> bool:
    return all(
        size == 1 or left == right
        for left, right, size in zip(
            stride, FlexibleLayout.contiguous_strides(shape), shape
        )
    )
