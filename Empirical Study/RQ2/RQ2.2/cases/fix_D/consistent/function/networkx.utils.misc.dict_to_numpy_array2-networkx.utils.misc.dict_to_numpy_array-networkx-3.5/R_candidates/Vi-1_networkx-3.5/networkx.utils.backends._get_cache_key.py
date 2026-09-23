def _get_cache_key(
    *,
    edge_attrs,
    node_attrs,
    preserve_edge_attrs,
    preserve_node_attrs,
    preserve_graph_attrs,
):
    """Return key used by networkx caching given arguments for ``convert_from_nx``."""
    # edge_attrs: dict | None
    # node_attrs: dict | None
    # preserve_edge_attrs: bool (False if edge_attrs is not None)
    # preserve_node_attrs: bool (False if node_attrs is not None)
    return (
        frozenset(edge_attrs.items())
        if edge_attrs is not None
        else preserve_edge_attrs,
        frozenset(node_attrs.items())
        if node_attrs is not None
        else preserve_node_attrs,
    )
