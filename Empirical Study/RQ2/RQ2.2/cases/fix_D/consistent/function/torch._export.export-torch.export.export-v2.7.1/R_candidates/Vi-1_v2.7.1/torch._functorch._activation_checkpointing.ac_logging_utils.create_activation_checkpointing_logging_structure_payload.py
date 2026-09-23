def create_activation_checkpointing_logging_structure_payload(
    joint_graph: Graph,
    joint_graph_node_information: dict[str, Any],
    joint_graph_edges: list[tuple[str, str]],
    all_recomputable_banned_nodes: list[Node],
    expected_runtime: float,
    saved_node_idxs: list[int],
    recomputable_node_idxs: list[int],
    memories_banned_nodes: list[float],
    runtimes_banned_nodes: list[float],
    min_cut_saved_values: list[Node],
) -> dict[str, Any]:
    activation_checkpointing_logging_structure_payload: dict[str, Any] = {
        "Joint Graph Size": len(joint_graph.nodes),
        "Joint Graph Edges": {
            "Total": len(joint_graph_edges),
            "Edges": joint_graph_edges,
        },
        "Joint Graph Node Information": joint_graph_node_information,
        "Recomputable Banned Nodes Order": [
            node.name for node in all_recomputable_banned_nodes
        ],
        "Expected Runtime": expected_runtime,
        "Knapsack Saved Nodes": saved_node_idxs,
        "Knapsack Recomputed Nodes": recomputable_node_idxs,
        "Knapsack Input Memories": memories_banned_nodes,
        "Knapsack Input Runtimes": runtimes_banned_nodes,
        "Min Cut Solution Saved Values": [node.name for node in min_cut_saved_values],
    }
    return activation_checkpointing_logging_structure_payload
