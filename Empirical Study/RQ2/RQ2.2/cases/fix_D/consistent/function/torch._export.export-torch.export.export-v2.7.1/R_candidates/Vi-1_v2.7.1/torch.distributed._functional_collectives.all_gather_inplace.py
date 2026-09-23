def all_gather_inplace(
    tensor_list: list[torch.Tensor],
    tensor: torch.Tensor,
    group=None,
    async_op=False,
    tag: str = "",
):
    assert not async_op, (
        "Can't remap async version of inplace op to functional collective"
    )
    assert all(t.size(0) == tensor.size(0) for t in tensor_list), (
        "Remapping variable size all_gather is not yet supported"
    )

    group = group or dist.group.WORLD
    assert group is not None

    output = all_gather_tensor(tensor, 0, group, tag)

    # Use aten.slice instead of aten.split because the latter causes
    # tensor.shape(0) to be unnecessarily baked in when it's a SymInt.
    output_splits = []
    offset = 0
    for t in tensor_list:
        output_splits.append(output[offset : offset + t.size(0)])
        offset += t.size(0)
    for dst, src in zip(tensor_list, output_splits):
        dst.copy_(src)
    return tensor_list
