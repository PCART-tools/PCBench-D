def reduce_scatter_tensor_autograd(
    self: torch.Tensor,
    reduceOp: str,
    scatter_dim: int,
    group: RANK_TYPES,
    tag: str = "",
):
    """
    Reduces the tensor data across all machines in such a way that all get
    the final result, then scatter the results to corresponding ranks.

    This function is the same as reduce_scatter_tensor but will propagate the
    backwards gradient across workers.

    Currently only the "sum" reduceOp is supported.

    See reduce_scatter_tensor for more details on usage.
    """

    group_name = _resolve_group_name(group, tag)
    group_size = c10d._get_group_size_by_name(group_name)

    assert self.size(scatter_dim) % group_size == 0, (
        f"input dimension 0 ({self.size(0)} must be a multiple of group_size {group_size}"
    )
    if scatter_dim != 0:
        tensor_list = torch.chunk(self, group_size, dim=scatter_dim)
        self = torch.cat(tensor_list)

    tensor = torch.ops._c10d_functional_autograd.reduce_scatter_tensor(
        self,
        reduceOp.lower(),
        group_size,
        group_name,  # type: ignore[possibly-undefined]
    )
    res = _FromTorchTensor.apply(tensor)
    return res
