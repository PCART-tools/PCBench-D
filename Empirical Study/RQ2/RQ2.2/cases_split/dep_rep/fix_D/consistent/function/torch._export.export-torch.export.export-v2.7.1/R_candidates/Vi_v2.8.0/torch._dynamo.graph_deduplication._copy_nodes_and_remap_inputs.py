def _copy_nodes_and_remap_inputs(
    subgraph: torch.fx.Graph, region: Region
) -> list[OrderedSet[UsageIndex]]:
    external_input_to_usages = _get_external_inputs(region)
    external_node_usages = list[OrderedSet[UsageIndex]]()
    region_to_subgraph_node = {}
    for node, usage_indices in external_input_to_usages.items():
        placeholder = subgraph.placeholder(f"subgraph_input_{node.name}")
        region_to_subgraph_node[node] = placeholder
        external_node_usages.append(usage_indices)

    def map_arg(node: Node) -> Node:
        if node in region_to_subgraph_node:
            return region_to_subgraph_node[node]
        else:
            return node

    for node in region:
        subgraph_node = subgraph.node_copy(node, lambda old: map_arg(old))
        region_to_subgraph_node[node] = subgraph_node

    return external_node_usages
