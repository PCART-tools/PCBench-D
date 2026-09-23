def insert_weight_and_bias_get_attr_node_from_get_attr_to_qtensor(
    gm: torch.fx.GraphModule,
    get_attr_to_weight_node: torch.fx.Node,
    get_attr_to_bias_node: Optional[torch.fx.Node],
) -> tuple[torch.fx.Node, Optional[torch.fx.Node]]:
    assert isinstance(get_attr_to_weight_node.target, str)
    w_qtensor = getattr(gm, get_attr_to_weight_node.target)
    w_attr_name = f"dequantized_{get_attr_to_weight_node.target}_w"

    if get_attr_to_bias_node is not None:
        assert isinstance(get_attr_to_bias_node.target, str)
        b_qtensor = getattr(gm, get_attr_to_bias_node.target)
        b_attr_name = f"dequantized_{get_attr_to_bias_node.target}_b"
    else:
        b_qtensor, b_attr_name = None, ""

    return insert_weight_and_bias_get_attr_node(
        gm, w_qtensor, b_qtensor, w_attr_name, b_attr_name
    )
