def is_acc_op(node_or_target: Union[Callable, torch.fx.Node]) -> bool:
    """
    Returns whether `node_or_target` is an acc_op. If it's a node, then checks whether
    it's a call_function target is from the acc_ops module. Otherwise it's already
    the target, which is similarly checked to see if it's from the acc_ops module.
    """
    if isinstance(node_or_target, torch.fx.Node):
        # All acc_ops are call_functions.
        if node_or_target.op != "call_function":
            return False
        target = node_or_target.target
    else:
        target = node_or_target
    return "acc_ops" in target.__module__
