def add_optimization_properties_to_meta(mod: torch.fx.GraphModule) -> None:
    """
    Add acc_op properties to Node.meta to inform optimization
    """
    for node in mod.graph.nodes:
        node.meta['acc_op_properties'] = acc_op_properties[node.target]
