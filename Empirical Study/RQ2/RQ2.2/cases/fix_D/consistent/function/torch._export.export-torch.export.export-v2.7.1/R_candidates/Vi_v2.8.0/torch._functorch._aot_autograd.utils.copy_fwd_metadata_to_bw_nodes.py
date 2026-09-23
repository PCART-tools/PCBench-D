def copy_fwd_metadata_to_bw_nodes(fx_g):
    """
    Input: `fx_g` which contains the joint fwd+bwd FX graph created by
    aot_autograd.

    This function walks the graph and copies over metadata from forward nodes
    to backward nodes, using the `seq_nr` field as a one-to-many mapping
    from forward node to backward node. This metadata is useful for performance
    profiling and debugging.
    """

    def _is_forward_node_with_seq_nr(node):
        # For now, assume that if nn_module_stack_metadata is populated, this
        # node is from the forward. Ignore nodes without `seq_nr`.
        # TODO(future): there is likely a less brittle way to do this by walking
        # the descendants of graph inputs corresponding to fwd inputs, didn't
        # seem obvious at first glance on how to partition graph inputs into
        # fwd vs bwd without relying on string names.
        return "nn_module_stack" in node.meta and "seq_nr" in node.meta

    def _is_backward_node_with_seq_nr(node):
        # For now, assume that if nn_module_stack_metadata is not populated,
        # this node is from the backward. Ignore nodes without `seq_nr`.
        # TODO(future): there is likely a less brittle way to do this, same
        # as with the forward.
        return ("nn_module_stack" not in node.meta) and "seq_nr" in node.meta

    fwd_seq_nr_to_node = {}
    for node in fx_g.graph.nodes:
        if not _is_forward_node_with_seq_nr(node):
            continue
        seq_nr = node.meta["seq_nr"]
        if seq_nr in fwd_seq_nr_to_node:
            # If we already saw an op with the current `seq_nr`, that means
            # that the current op did not create an autograd node, and there
            # is no corresponding backward node, so we skip.
            continue
        fwd_seq_nr_to_node[node.meta["seq_nr"]] = node

    for node in fx_g.graph.nodes:
        if not _is_backward_node_with_seq_nr(node):
            continue
        # fwd_node should always exist, but handle non-existence just in case
        fwd_node = fwd_seq_nr_to_node.get(node.meta["seq_nr"])
        if fwd_node is not None:
            node.meta["fwd_nn_module_stack"] = fwd_node.meta["nn_module_stack"]
            node.meta["fwd_source_fn_stack"] = fwd_node.meta.get("source_fn_stack")
