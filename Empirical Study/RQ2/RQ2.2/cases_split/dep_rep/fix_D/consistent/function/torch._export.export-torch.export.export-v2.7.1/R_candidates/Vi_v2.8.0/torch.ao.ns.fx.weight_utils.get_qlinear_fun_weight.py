def get_qlinear_fun_weight(node: Node, gm: GraphModule) -> torch.Tensor:
    # packed weight is arg 1
    packed_weight_node = node.args[1]
    assert isinstance(packed_weight_node, Node)
    assert packed_weight_node.op == "get_attr"
    packed_weight = getattr_from_fqn(gm, packed_weight_node.target)  # type: ignore[arg-type]
    # TODO(future PR): why does packed_weight.unpack() not work?
    (weight, _bias), _name = packed_weight.__getstate__()
    return weight
