def _recursive_joint_graph_passes(
    gm: GraphModule, skip_invoke_subgraph: bool = False
) -> None:
    with dynamo_timed(
        "_recursive_joint_graph_passes",
        log_pt2_compile_event=True,
        dynamo_compile_column_us="joint_graph_pass_time_us",
    ):
        # invoke_subgraph already runs the _recursive_joint_graph_passes.  In
        # AOTAutograd, `run_joint_graph_passes_on_hops` partitions the
        # invoke_subgraph HOP before calling the partitioner on the outer graph.
        # AOTAutograd has access to partition_fn, which internally calls the
        # `_recursive_joint_graph_passes` for the subgraph. So, skip recursing
        # skip_invoke_subgraph.
        for subgraph_name in _get_subgraph_names(gm, skip_invoke_subgraph):
            subgraph = getattr(gm, subgraph_name)
            _recursive_joint_graph_passes(subgraph, skip_invoke_subgraph)
        joint_graph_passes(gm)
