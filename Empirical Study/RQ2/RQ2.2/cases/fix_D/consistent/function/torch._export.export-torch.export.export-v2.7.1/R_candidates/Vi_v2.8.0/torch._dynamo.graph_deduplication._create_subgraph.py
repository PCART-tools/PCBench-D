def _create_subgraph(
    region: Region,
    inds_with_external_users: list[int],
) -> tuple[torch.fx.Graph, list[OrderedSet[UsageIndex]]]:
    subgraph: torch.fx.Graph = torch.fx.Graph()
    external_node_usages = _copy_nodes_and_remap_inputs(subgraph, region)
    _create_subgraph_outputs(subgraph, inds_with_external_users)
    return subgraph, external_node_usages
