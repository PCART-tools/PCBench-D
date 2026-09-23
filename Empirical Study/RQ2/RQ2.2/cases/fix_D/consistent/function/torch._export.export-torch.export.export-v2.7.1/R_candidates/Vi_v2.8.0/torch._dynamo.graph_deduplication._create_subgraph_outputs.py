def _create_subgraph_outputs(
    subgraph: torch.fx.Graph, inds_to_output: list[int]
) -> None:
    node_list = [n for n in subgraph.nodes if n.op not in ("placeholder", "output")]
    out_tup = tuple(node_list[ind] for ind in inds_to_output)
    subgraph.output(out_tup)
