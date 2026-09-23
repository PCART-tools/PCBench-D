def get_collective_group_size(node: ir.IRNode) -> int:
    if type(node) == ir._CollectiveKernel:
        from torch.distributed.distributed_c10d import _get_group_size_by_name

        return _get_group_size_by_name(node.constant_args[-1])
    else:
        raise TypeError(f"Unsupported collective type: {node}")
