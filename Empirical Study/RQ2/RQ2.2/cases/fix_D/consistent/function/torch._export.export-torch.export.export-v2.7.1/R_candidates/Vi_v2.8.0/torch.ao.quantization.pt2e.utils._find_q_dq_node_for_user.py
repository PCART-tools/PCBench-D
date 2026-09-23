def _find_q_dq_node_for_user(
    produer: torch.fx.Node, user: torch.fx.Node
) -> tuple[Any, Any]:
    """
    Find q, dq pair corresponding to [producer -> q -> dq -> user]
    Utils works by finding dq arg of user and ensuring it is connected to
    producer
    """
    dq_node = None
    for n in user.args:
        if (
            isinstance(n, torch.fx.Node)
            and n.op == "call_function"
            and n.target in _DEQUANTIZE_OPS
        ):
            if _is_connected(produer, n):
                dq_node = n
                break
    if dq_node is None:
        for n in user.kwargs:
            if (
                isinstance(n, torch.fx.Node)
                and n.op == "call_function"
                and n.target in _DEQUANTIZE_OPS
            ):
                if _is_connected(produer, n):
                    dq_node = n
                    break
    if dq_node is None:
        return (None, None)

    q_node = None
    if (
        isinstance(arg := dq_node.args[0], torch.fx.Node)
        and arg.op == "call_function"
        and arg.target in _QUANTIZE_OPS
    ):
        q_node = arg
    return (q_node, dq_node)
