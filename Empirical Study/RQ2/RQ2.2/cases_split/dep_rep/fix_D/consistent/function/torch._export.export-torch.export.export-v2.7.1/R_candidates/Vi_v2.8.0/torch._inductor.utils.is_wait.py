def is_wait(node: Optional[Union[IRNode, Operation]]) -> bool:
    from . import ir

    return type(node) == ir._WaitKernel
