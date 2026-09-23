def maybe_propagate_dtype_for_node(
    node: Node,
    target_dtype: torch.dtype,
    node_name_to_target_dtype: Dict[str, torch.dtype],
    matches: Dict[str, MatchResult],
) -> None:
    """
    Assigns `target_dtype` to `node`. If `node` is a general tensor shape op
    (see GeneralTensorShapeOpQuantizeHandler in quantization_patterns.py for more details)
    also call this function recursively on
    the first argument, to propagate the dtype to the caller.
    """
    node_name_to_target_dtype[node.name] = target_dtype
    # if this is a copy node, propagate to first arg
    root_node, matched_nodes, pattern, qhandler, qconfig = matches.get(
        node.name, (None, None, None, None, None))
    if qhandler is not None and qhandler.is_general_tensor_shape_op():
        prev_node = node.args[0]
        if isinstance(prev_node, Node):
            maybe_propagate_dtype_for_node(
                prev_node, target_dtype, node_name_to_target_dtype, matches)
