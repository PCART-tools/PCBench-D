@register_decomposition([aten.index_add])
def index_add(
    x: torch.Tensor,
    dim: int,
    index: torch.Tensor,
    tensor: torch.Tensor,
    *,
    alpha: torch.types.Number = 1,
) -> torch.Tensor:
    # If we are not in fbcode and dtype is bfloat16
    # fallback to index_add kernel
    # see https://github.com/pytorch/pytorch/issues/137425 for details
    if not is_fbcode() and x.dtype == torch.bfloat16:
        return NotImplemented
    else:
        return _index_add(x, dim, index, tensor, inplace=False, alpha=alpha)
