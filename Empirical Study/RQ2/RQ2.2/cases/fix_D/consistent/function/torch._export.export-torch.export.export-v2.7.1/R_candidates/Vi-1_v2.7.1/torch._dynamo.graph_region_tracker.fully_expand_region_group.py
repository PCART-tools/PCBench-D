def fully_expand_region_group(
    regions: list[Region],
    seen_nodes: set[Node],
    is_identical_fn: Callable[[Node, Node], bool],
) -> None:
    debug_log("--------------------------------------------------")
    debug_log("expanding new region group: %s", regions)

    # All regions should start with 1 node
    assert all(len(region) == 1 for region in regions)
    region_iters = []
    for region in regions:
        (origin,) = region  # Only works for 1 element sets
        region_iters.append(BackwardBfsArgIter.create(origin))

    nodes_to_add: list[Node] = []

    # we already have the origin node in each region
    for region_it in region_iters:
        node = region_it.next()
        assert node
        region_it.add_children(node)

    current_node = region_iters[0].next()
    assert current_node is not None
    # Loop incrementally adding new nodes to each region
    # regions are only expanded if the node to add is valid
    # for ALL regions
    while current_node:
        add_node = True
        nodes_to_add.clear()
        nodes_to_add.append(current_node)
        nodes_to_add_set = set(nodes_to_add)
        for region_it in region_iters[1:]:
            node = region_it.next()

            debug_log("--------------------")
            debug_log("considering adding: %s, cur_node: %s", node, current_node)
            debug_log("previously claimed nodes: %s", node in seen_nodes)
            debug_log("%s", seen_nodes)
            if node:
                debug_log("is_identical: %s", is_identical_fn(node, current_node))
                add_node &= (
                    node not in seen_nodes
                    and node not in nodes_to_add_set
                    and node.op != "placeholder"
                    and is_identical_fn(node, current_node)
                )
                nodes_to_add.append(node)
                nodes_to_add_set.add(node)
            else:
                add_node = False

            debug_log("--------------------")

        if add_node:
            for region, region_it, node in zip(regions, region_iters, nodes_to_add):
                region.append(node)
                debug_log("adding %s's children", node)
                debug_log("%s %s", node.args, list(node.kwargs.items()))
                region_it.add_children(node)
                seen_nodes.add(node)

        current_node = region_iters[0].next()

    # Ensure regions are sorted in topological order
    for region in regions:
        region.reverse()

    debug_log("end expand new region group: %s", regions)
    debug_log("--------------------------------------------------")
