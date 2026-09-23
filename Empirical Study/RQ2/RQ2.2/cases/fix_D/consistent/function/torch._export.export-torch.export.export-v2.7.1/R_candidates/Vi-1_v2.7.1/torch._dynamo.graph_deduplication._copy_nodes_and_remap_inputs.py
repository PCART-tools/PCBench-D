def _copy_nodes_and_remap_inputs(
    subgraph: torch.fx.Graph, region: Region
) -> dict[tuple[int, int], Any]:
    external_inputs_to_indices = _get_external_inputs(region)
    indices_to_placeholder_ind: dict[tuple[int, int], Any] = {}
    region_to_subgraph_node = {}
    for node in external_inputs_to_indices.keys():
        placeholder = subgraph.placeholder(f"subgraph_input_{node.name}")
        region_to_subgraph_node[node] = placeholder
        arg_indices = external_inputs_to_indices[node]
        # Note: insertion order matches the order in which placeholders were created
        # for the calling convention of the subgraph
        indices_to_placeholder_ind[arg_indices] = None

    def map_arg(node: Node) -> Node:
        if node in region_to_subgraph_node:
            return region_to_subgraph_node[node]
        else:
            return node

    for node in region:
        subgraph_node = subgraph.node_copy(node, lambda old: map_arg(old))
        region_to_subgraph_node[node] = subgraph_node

    return indices_to_placeholder_ind
