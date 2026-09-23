def is_cudagraph_unsafe_op(node: Operation) -> bool:
    """
    Returns True if the node is an op that is not cudagraphable.
    Usually only custom ops have this tag.
    """
    from . import ir

    if not isinstance(node, ir.FallbackKernel):
        return False

    if (
        isinstance(node.op_overload, torch._ops.OpOverload)
        and torch._C.Tag.cudagraph_unsafe in node.op_overload.tags
    ):
        return True

    return False
