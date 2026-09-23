def _replace_region_with_subgraph(
    graph: torch.fx.Graph,
    region: Region,
    get_subgraph_node: Node,
    external_node_usages: Iterable[OrderedSet[UsageIndex]],
    inds_with_external_users: list[int],
    subgraph_name: str,
    node_to_additional_deps: dict[Node, OrderedSet[Node]],
    node_to_mutated_arg_positions: dict[Node, OrderedSet[int]],
) -> None:
    sub_args = []
    for usages in external_node_usages:
        node_ind, usage_ind = next(iter(usages))
        node = region[node_ind]
        flattened_args_kwargs = _get_flat_args(node, {})
        for user_ind, node_usage_ind in usages:
            user = region[user_ind]
            if user in node_to_mutated_arg_positions:
                if node_usage_ind in node_to_mutated_arg_positions[user]:
                    log.debug(
                        "NYI: Failed to substitute region %s due to mutation", region
                    )
                    return
        sub_args.append(flattened_args_kwargs[usage_ind])

    # Input/Output aliasing not supported in HOPs today
    # Note: we should use the nodes in the original graph (the region here)
    # because we use the original traced example values for this check
    if _has_aliasing(region, sub_args, inds_with_external_users):
        return

    invoke_args = (get_subgraph_node, subgraph_name, *sub_args)

    invoke_subgraph_node = graph.create_node(
        "call_function",
        torch.ops.higher_order.invoke_subgraph,
        invoke_args,  # type: ignore[arg-type]
        {},
    )
    for ind, external_user_ind in enumerate(inds_with_external_users):
        node = region[external_user_ind]
        subgraph_output = graph.create_node(
            "call_function", operator.getitem, (invoke_subgraph_node, ind), {}
        )
        node.replace_all_uses_with(subgraph_output, propagate_meta=True)

    # Erase in reverse topological order
    for node in reversed(region):
        graph.erase_node(node)
        # Remove any nodes with additional deps
        # This is safe; we've guaranteed that there is
        # no input mutation, so all additional deps
        # will be internal to the subgraph
        node_to_additional_deps.pop(node, None)
        for deps in node_to_additional_deps.values():
            try:
                deps.remove(node)
                deps.add(invoke_subgraph_node)
            except KeyError:
                pass

    if config.graph_deduplication_lint:
        print(_detect_cycles(graph, node_to_additional_deps))
        _stable_topological_sort(graph, node_to_additional_deps)
        graph.lint()
