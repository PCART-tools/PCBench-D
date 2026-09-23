def get_qconv_fun_weight(node: Node, gm: GraphModule) -> torch.Tensor:
    # qconv state is arg 1
    qconv_state_node = node.args[1]
    assert isinstance(qconv_state_node, Node)
    assert qconv_state_node.op == 'get_attr'
    qconv_state_obj = getattr_from_fqn(gm, qconv_state_node.target)  # type: ignore[arg-type]
    return qconv_state_obj.weight()
