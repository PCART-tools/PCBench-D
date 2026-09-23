def graphviz_layout(G, prog="neato", root=None):
    """Create node positions using Pydot and Graphviz.

    Returns a dictionary of positions keyed by node.

    Parameters
    ----------
    G : NetworkX Graph
        The graph for which the layout is computed.
    prog : string (default: 'neato')
        The name of the GraphViz program to use for layout.
        Options depend on GraphViz version but may include:
        'dot', 'twopi', 'fdp', 'sfdp', 'circo'
    root : Node from G or None (default: None)
        The node of G from which to start some layout algorithms.

    Returns
    -------
      Dictionary of (x, y) positions keyed by node.

    Examples
    --------
    >>> G = nx.complete_graph(4)
    >>> pos = nx.nx_pydot.graphviz_layout(G)
    >>> pos = nx.nx_pydot.graphviz_layout(G, prog="dot")

    Notes
    -----
    This is a wrapper for pydot_layout.
    """
    msg = (
        "nx.nx_pydot.graphviz_layout depends on the pydot package, which has"
        "known issues and is not actively maintained. Consider using"
        "nx.nx_agraph.graphviz_layout instead.\n\n"
        "See https://github.com/networkx/networkx/issues/5723"
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)

    return pydot_layout(G=G, prog=prog, root=root)
