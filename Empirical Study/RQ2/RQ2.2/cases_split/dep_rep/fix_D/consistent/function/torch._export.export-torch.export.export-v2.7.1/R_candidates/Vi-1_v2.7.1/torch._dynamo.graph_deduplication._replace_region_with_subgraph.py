def _replace_region_with_subgraph(
    graph: torch.fx.Graph,
    region: Region,
    get_subgraph_node: Node,
    node_ind_arg_ind: Iterable[tuple[int, int]],
    inds_with_external_users: list[int],
    sub_gm: torch.fx.GraphModule,
    subgraph_name: str,
    output_replacements: dict[Node, Node],
) -> None:
    sub_args = []
    for node_ind, arg_ind in node_ind_arg_ind:
        node = region[node_ind]
        flattened_args_kwargs = _flatten_args_kwargs((node.args, node.kwargs))
        sub_args.append(flattened_args_kwargs[arg_ind])

    invoke_args = (get_subgraph_node, subgraph_name, tuple(sub_args))
    fake_inputs = [node.meta["example_value"] for node in sub_args]

    if has_potential_input_alias_or_mutation(sub_gm, fake_inputs):
        log.debug(
            "NYI: Failed to substitute region %s due to input alias or mutation",
            region,
        )
        return

    latest_region_node = region[-1]
    with graph.inserting_after(latest_region_node):
        invoke_subgraph_node = graph.create_node(
            "call_function", torch.ops.higher_order.invoke_subgraph, invoke_args, {}
        )
        with graph.inserting_after(invoke_subgraph_node):
            for ind, external_user_ind in enumerate(inds_with_external_users):
                node = region[external_user_ind]
                subgraph_output = graph.create_node(
                    "call_function", operator.getitem, (invoke_subgraph_node, ind), {}
                )
                output_replacements[node] = subgraph_output
                node.replace_all_uses_with(subgraph_output, propagate_meta=True)

        # Erase in reverse topological order
        for node in reversed(region):
            graph.erase_node(node)
