def is_collective(
    node: Optional[Union[Node, Operation]],
    op: Optional[torch._ops.OperatorBase] = None,
) -> bool:
    if node is None:
        return False

    from . import ir

    return (
        type(node) == ir._CollectiveKernel and (op is None or node.op_overload is op)
    ) or (
        # TODO: this is a temporary solution to ensure that we can identify torchrec's
        # communication ops. But in order to allow better communication and computation
        # overlap, torchrec's communication ops should be not used.
        type(node) == ir.FallbackKernel
        and (
            # NOTE: the `hasattr()` check is to bypass errors such as the following:
            # AttributeError: '_OpNamespace' 'torchrec' object has no attribute 'all_to_all_single'
            (
                hasattr(torch.ops.torchrec, "all_to_all_single")
                and node.op_overload == torch.ops.torchrec.all_to_all_single.default
            )
            or (
                hasattr(torch.ops.torchrec, "all_gather_into_tensor")
                and node.op_overload
                == torch.ops.torchrec.all_gather_into_tensor.default
            )
            or (
                hasattr(torch.ops.torchrec, "reduce_scatter_tensor")
                and node.op_overload == torch.ops.torchrec.reduce_scatter_tensor.default
            )
        )
    )
