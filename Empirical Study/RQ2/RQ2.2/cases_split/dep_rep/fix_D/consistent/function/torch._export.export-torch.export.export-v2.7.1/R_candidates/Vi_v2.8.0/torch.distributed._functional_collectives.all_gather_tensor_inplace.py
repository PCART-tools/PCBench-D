def all_gather_tensor_inplace(
    output_tensor: torch.Tensor,
    input_tensor: torch.Tensor,
    group=None,  # TODO add a type,
    async_op: bool = False,
    tag: str = "",
    gather_dim: int = 0,
):
    assert not async_op, (
        "Can't remap async version of inplace op to functional collective"
    )

    group = group or dist.group.WORLD
    assert group is not None

    return output_tensor.copy_(all_gather_tensor(input_tensor, gather_dim, group, tag))
