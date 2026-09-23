def _is_set_grad_enabled_node(node: torch.fx.Node) -> Union[torch.fx.Node, bool]:
    return (
        node
        and node.op == "call_function"
        and node.target == torch._C._set_grad_enabled
    )
