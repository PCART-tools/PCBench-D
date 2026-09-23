def is_acc_op_with_kwarg(
    node_or_target: Union[Callable, torch.fx.Node], kwarg: str
) -> bool:
    """
    Helper that inspects `node_or_target` and returns whether it is an acc_op node
    (or a target for an acc_op) that has an arg signature that includes `kwarg`.
    """
    if not is_acc_op(node_or_target):
        return False

    target = (
        node_or_target.target
        if isinstance(node_or_target, torch.fx.Node)
        else node_or_target
    )
    assert not isinstance(target, str)
    return kwarg in inspect.signature(inspect.unwrap(target)).parameters
