def _update_shared_with(
    child: EdgeOrNode,
    qspec: QuantizationSpecBase,
    shared_with_map: dict[EdgeOrNode, EdgeOrNode],
):
    """Update the `shared_with_map` based on the qspec, this applies the `SharedQuantizationSpec`
    configuration and established the relationship between `edge_or_node` with the edge/node that it
    is pointing to, we'll use this information in the end to get the group id
    """
    if isinstance(qspec, SharedQuantizationSpec):
        parent = qspec.edge_or_node
        # we point from edge_or_node to the node that it is sharing_with, e.g.
        # qspec for a = SharedQuantizationSpec(b) means `a` points to `b`
        _union(parent, child, shared_with_map)
