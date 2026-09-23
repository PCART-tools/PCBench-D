@out_wrapper()
def index_add(
    x: TensorLike,
    dim: int,
    index: TensorLike,
    tensor: TensorLike,
    *,
    alpha: NumberType = 1,
):
    # index_add always returns a new contiguous tensor
    return x.clone(memory_format=torch.contiguous_format).index_add_(
        dim,
        index,
        tensor,
        alpha=alpha,  # type: ignore[arg-type]
    )
