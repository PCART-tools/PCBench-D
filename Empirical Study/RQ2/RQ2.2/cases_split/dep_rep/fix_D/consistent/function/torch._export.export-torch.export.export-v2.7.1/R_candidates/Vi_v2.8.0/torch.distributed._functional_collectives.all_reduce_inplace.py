def all_reduce_inplace(
    tensor: torch.Tensor,
    op: str = "sum",
    group=None,
    async_op: bool = False,
    tag: str = "",
):
    assert not async_op, (
        "Can't remap async version of inplace op to functional collective"
    )

    group = group or dist.group.WORLD
    assert group is not None

    return tensor.copy_(all_reduce(tensor, op, group, tag))
