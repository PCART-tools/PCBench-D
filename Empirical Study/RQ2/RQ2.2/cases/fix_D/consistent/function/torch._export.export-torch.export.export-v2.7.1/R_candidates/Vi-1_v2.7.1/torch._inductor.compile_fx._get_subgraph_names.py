def _get_subgraph_names(gm: GraphModule) -> Generator[str, None, None]:
    for node in sorted(
        itertools.chain(
            gm.graph.find_nodes(op="call_function", target=torch.ops.higher_order.cond),
            gm.graph.find_nodes(
                op="call_function", target=torch.ops.higher_order.while_loop
            ),
        )
    ):
        if node.target == torch.ops.higher_order.cond:
            true_subgraph_name = node.args[1].name
            false_subgraph_name = node.args[2].name
            yield true_subgraph_name
            yield false_subgraph_name
        elif node.target == torch.ops.higher_order.while_loop:
            cond_subgraph_name = node.args[0].name
            body_subgraph_name = node.args[1].name
            yield cond_subgraph_name
            yield body_subgraph_name
