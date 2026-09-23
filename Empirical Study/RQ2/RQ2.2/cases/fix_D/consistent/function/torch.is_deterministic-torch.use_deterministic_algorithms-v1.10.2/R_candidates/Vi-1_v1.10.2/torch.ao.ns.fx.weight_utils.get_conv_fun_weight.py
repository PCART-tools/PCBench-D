def get_conv_fun_weight(node: Node, gm: GraphModule) -> torch.Tensor:
    # traverse backwards from the weight arg, accounting for any observers
    weight_arg_node = node.args[1]
    assert isinstance(weight_arg_node, Node)
    weight_node = return_first_non_observer_node(weight_arg_node, gm)
    assert isinstance(weight_node, Node)
    assert weight_node.op == 'get_attr'
    weight = getattr_from_fqn(gm, weight_node.target)  # type: ignore[arg-type]
    return weight.detach()
