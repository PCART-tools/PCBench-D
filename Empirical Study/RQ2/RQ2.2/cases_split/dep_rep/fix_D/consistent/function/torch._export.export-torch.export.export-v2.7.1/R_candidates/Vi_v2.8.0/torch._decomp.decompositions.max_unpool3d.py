@register_decomposition(aten.max_unpool3d)
@out_wrapper()
def max_unpool3d(
    input: TensorLike,
    indices: TensorLike,
    output_size: list[int],
    stride: list[int],
    padding: list[int],
):
    torch._check(
        indices.dtype == torch.int64, lambda: "elements in indices should be type int64"
    )
    torch._check(
        input.ndim in (4, 5),
        lambda: f"Input to max_unpooling3d should be a 4d or 5d Tensor, but got a tensor with {input.ndim} dimensions.",
    )
    torch._check(
        len(output_size) == 3,
        lambda: (
            f"There should be exactly three elements (depth, height, width) in output_size, "
            f"but got {len(output_size)} elements."
        ),
    )
    torch._check(
        len(stride) == 3,
        lambda: f"There should be exactly three elements (depth, height, width) in stride, but got: {len(stride)} elements.",
    )
    torch._check(
        len(padding) == 3,
        lambda: f"There should be exactly three elements (depth, height, width) in padding, but got: {len(padding)} elements.",
    )
    torch._check(
        input.shape == indices.shape,
        lambda: (
            f"Expected shape of indices to be same as that of the input tensor ({input.shape}) "
            f"but got indices tensor with shape: {indices.shape}"
        ),
    )

    for i in range(1, input.ndim):
        torch._check(
            input.size(i) > 0,
            lambda: (
                f"max_unpooling3d(): "
                f"Expected input to have non-zero size for non-batch dimensions, "
                f"but got {input.shape} with dimension {i} being empty."
            ),
        )

    torch._check(
        stride[0] > 0 and stride[1] > 0 and stride[2] > 0,
        lambda: f"strides should be greater than zero, but got stride: {stride}",
    )

    return _max_unpoolnd(input, indices, output_size, 3)
