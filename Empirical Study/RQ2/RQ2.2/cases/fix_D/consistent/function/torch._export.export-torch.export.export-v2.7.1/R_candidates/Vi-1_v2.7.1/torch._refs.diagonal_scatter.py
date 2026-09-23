@register_decomposition(aten.diagonal_scatter)
@out_wrapper()
def diagonal_scatter(
    input: TensorLikeType,
    src: TensorLikeType,
    offset: int = 0,
    dim1: int = 0,
    dim2: int = 1,
) -> TensorLikeType:
    out = utils.clone_preserve_strides(input)
    diag = out.diagonal(offset, dim1, dim2)
    torch._check(
        diag.shape == src.shape,
        lambda: "expected src to have a size equal to the diagonal of the input."
        f"Got {src.shape} for a diagonal of shape {diag.shape}",
    )
    copy_to(diag, src)
    return out
