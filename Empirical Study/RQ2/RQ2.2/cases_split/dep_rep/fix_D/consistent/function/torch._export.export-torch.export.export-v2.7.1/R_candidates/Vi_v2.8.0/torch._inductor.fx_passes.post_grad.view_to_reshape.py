def view_to_reshape(gm):
    """
    Replace view ops in the GraphModule to reshape ops.
    """
    subgraph_names: OrderedSet[str] = OrderedSet(
        x.target for x in gm.graph.find_nodes(op="get_attr")
    )

    for child_name, child_mod in gm.named_children():
        if child_name in subgraph_names and isinstance(child_mod, torch.fx.GraphModule):
            view_to_reshape(child_mod)

    for nd in gm.graph.find_nodes(
        op="call_function", target=torch.ops.aten.view.default
    ):
        nd.target = torch.ops.aten.reshape.default
