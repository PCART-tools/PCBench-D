def propagate_dtypes_for_known_nodes(
    graph: Graph,
    node_name_to_target_dtype: Dict[str, Dict[str, Optional[torch.dtype]]],
    matches: Dict[str, MatchResult],
) -> None:
    """
    Currently we assume that inputs to the graph are either `torch.float` or
    `torch.quint8`, which is not always correct. For ops such as
    `x.masked_fill(mask, value)`, we know that the dtype of  `mask` is a
    `BoolTensor`. Propagate this information throughout the graph.

    Note: not all dtypes in the graph will be correct after this pass, but a
    higher percentage of them will be correct. Hopefully in the future we can
    replace this with a better way to reason about dtypes of tensors.
    """
    for node in graph.nodes:
        bool_arg_idxs = node_bool_tensor_arg_indexes(node)
        for bool_arg_idx in bool_arg_idxs:
            cur_node = node.args[bool_arg_idx]
            maybe_propagate_dtype_for_node(
                cur_node, torch.bool, node_name_to_target_dtype, matches)
