def _recursive_joint_graph_passes(gm: GraphModule) -> None:
    with dynamo_timed(
        "_recursive_joint_graph_passes",
        log_pt2_compile_event=True,
        dynamo_compile_column_us="joint_graph_pass_time_us",
    ):
        for subgraph_name in _get_subgraph_names(gm):
            subgraph = getattr(gm, subgraph_name)
            _recursive_joint_graph_passes(subgraph)
        joint_graph_passes(gm)
