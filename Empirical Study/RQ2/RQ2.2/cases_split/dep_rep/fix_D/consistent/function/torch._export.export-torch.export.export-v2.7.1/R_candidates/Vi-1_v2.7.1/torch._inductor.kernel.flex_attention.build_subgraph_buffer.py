def build_subgraph_buffer(args: list[TensorBox], subgraph: Subgraph) -> SubgraphResults:
    return build_subgraph_module_buffer(args, subgraph.graph_module)
