def _union_input_edge_with(
    input_edge,
    input_edge_root_qspec,
    edge_or_node,
    edge_or_node_to_qspec,
    shared_with_map,
):
    """Union input edge with another edge or node, used in implicit sharing to point the current input
    edge to other user edges of the producer node, or the output of producer node since these are
    referring to the same Tensor
    """
    root_qspec = None
    if edge_or_node in edge_or_node_to_qspec:
        qspec = edge_or_node_to_qspec[edge_or_node]
        root_qspec = _unwrap_shared_qspec(qspec, edge_or_node_to_qspec, shared_with_map)
    # TODO: add assertions for types of root qspecs
    if root_qspec is not None and all(
        _has_same_attr(root_qspec, input_edge_root_qspec, attr)
        for attr in [
            "dtype",
            "is_dynamic",
            "quant_min",
            "quant_max",
            "qscheme",
            "ch_axis",
            "scale",
            "zero_point",
        ]
    ):
        # the input arg to the node should reuse the existing output observer for arg
        # since dtype is the same (we may want to extend this to be a more strict check
        # in the future)
        # so we point from `input_edge` to `arg` (output of the argument)
        _union(edge_or_node, input_edge, shared_with_map)
