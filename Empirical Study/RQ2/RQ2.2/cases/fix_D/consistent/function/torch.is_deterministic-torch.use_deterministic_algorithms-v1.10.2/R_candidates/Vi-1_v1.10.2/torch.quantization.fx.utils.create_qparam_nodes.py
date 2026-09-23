def create_qparam_nodes(
        node_name: str,
        scale: Any,
        zero_point: Any,
        modules: Dict[str, torch.nn.Module],
        quantized_graph: Graph,
        node_name_to_scope: Dict[str, Tuple[str, type]]
) -> Tuple[Node, Node]:
    """
    Create getattr nodes in the quantized graph for scale and zero point values.
    The nodes are registered with the root_module of the model.
    """
    root_module = modules['']
    module_path, _ = node_name_to_scope[node_name]
    scale_node = create_getattr_from_value(root_module, quantized_graph, (module_path + "_scale_"), scale)
    zero_point_node = create_getattr_from_value(root_module, quantized_graph, (module_path + "_zero_point_"), zero_point)
    return (scale_node, zero_point_node)
