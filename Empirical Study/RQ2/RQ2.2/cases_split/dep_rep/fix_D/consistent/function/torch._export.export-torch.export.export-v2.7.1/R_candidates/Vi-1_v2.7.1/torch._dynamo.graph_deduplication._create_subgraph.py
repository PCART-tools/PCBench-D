def _create_subgraph(
    region: Region,
    inds_with_external_users: list[int],
) -> tuple[torch.fx.Graph, dict[tuple[int, int], Any]]:
    subgraph: torch.fx.Graph = torch.fx.Graph()
    node_ind_input_inds = _copy_nodes_and_remap_inputs(subgraph, region)
    _create_subgraph_outputs(subgraph, inds_with_external_users)
    return subgraph, node_ind_input_inds
