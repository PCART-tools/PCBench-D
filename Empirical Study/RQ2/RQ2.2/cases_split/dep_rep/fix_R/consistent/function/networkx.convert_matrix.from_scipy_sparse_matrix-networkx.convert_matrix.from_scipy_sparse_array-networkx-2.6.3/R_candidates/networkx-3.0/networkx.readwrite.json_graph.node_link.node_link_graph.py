def node_link_graph(
    data,
    directed=False,
    multigraph=True,
    attrs=None,
    *,
    source="source",
    target="target",
    name="id",
    key="key",
    link="links",
):
    """Returns graph from node-link data format.
    Useful for de-serialization from JSON.

    Parameters
    ----------
    data : dict
        node-link formatted graph data

    directed : bool
        If True, and direction not specified in data, return a directed graph.

    multigraph : bool
        If True, and multigraph not specified in data, return a multigraph.

    attrs : dict
        A dictionary that contains five keys 'source', 'target', 'name',
        'key' and 'link'.  The corresponding values provide the attribute
        names for storing NetworkX-internal graph data.  Default value:

            dict(source='source', target='target', name='id',
                key='key', link='links')

        .. deprecated:: 2.8.6

           The `attrs` keyword argument will be replaced with the individual keywords: `source`, `target`, `name`,
           `key` and `link`. in networkx 3.2.

           If the `attrs` keyword and the new keywords are both used in a single function call (not recommended)
           the `attrs` keyword argument will take precedence.

           The values of the keywords must be unique.

    source : string
        A string that provides the 'source' attribute name for storing NetworkX-internal graph data.
    target : string
        A string that provides the 'target' attribute name for storing NetworkX-internal graph data.
    name : string
        A string that provides the 'name' attribute name for storing NetworkX-internal graph data.
    key : string
        A string that provides the 'key' attribute name for storing NetworkX-internal graph data.
    link : string
        A string that provides the 'link' attribute name for storing NetworkX-internal graph data.

    Returns
    -------
    G : NetworkX graph
        A NetworkX graph object

    Examples
    --------

    Create data in node-link format by converting a graph.

    >>> G = nx.Graph([('A', 'B')])
    >>> data = nx.node_link_data(G)
    >>> data
    {'directed': False, 'multigraph': False, 'graph': {}, 'nodes': [{'id': 'A'}, {'id': 'B'}], 'links': [{'source': 'A', 'target': 'B'}]}

    Revert data in node-link format to a graph.

    >>> H = nx.node_link_graph(data)
    >>> print(H.edges)
    [('A', 'B')]

    To serialize and deserialize a graph with JSON,

    >>> import json
    >>> d = json.dumps(node_link_data(G))
    >>> H = node_link_graph(json.loads(d))
    >>> print(G.edges, H.edges)
    [('A', 'B')] [('A', 'B')]


    Notes
    -----
    Attribute 'key' is only used for multigraphs.

    To use `node_link_data` in conjunction with `node_link_graph`,
    the keyword names for the attributes must match.

    See Also
    --------
    node_link_data, adjacency_data, tree_data
    """
    # ------ TODO: Remove between the lines after signature change is complete ----- #
    if attrs is not None:
        import warnings

        msg = (
            "\n\nThe `attrs` keyword argument of node_link_graph is deprecated\n"
            "and will be removed in networkx 3.2. It is replaced with explicit\n"
            "keyword arguments: `source`, `target`, `name`, `key` and `link`.\n"
            "To make this warning go away, and ensure usage is forward\n"
            "compatible, replace `attrs` with the keywords. "
            "For example:\n\n"
            "   >>> node_link_graph(data, attrs={'target': 'foo', 'name': 'bar'})\n\n"
            "should instead be written as\n\n"
            "   >>> node_link_graph(data, target='foo', name='bar')\n\n"
            "in networkx 3.2.\n"
            "The default values of the keywords will not change.\n"
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)

        source = attrs.get("source", "source")
        target = attrs.get("target", "target")
        name = attrs.get("name", "name")
        key = attrs.get("key", "key")
        link = attrs.get("link", "links")
    # -------------------------------------------------- #
    multigraph = data.get("multigraph", multigraph)
    directed = data.get("directed", directed)
    if multigraph:
        graph = nx.MultiGraph()
    else:
        graph = nx.Graph()
    if directed:
        graph = graph.to_directed()

    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else key
    graph.graph = data.get("graph", {})
    c = count()
    for d in data["nodes"]:
        node = _to_tuple(d.get(name, next(c)))
        nodedata = {str(k): v for k, v in d.items() if k != name}
        graph.add_node(node, **nodedata)
    for d in data[link]:
        src = tuple(d[source]) if isinstance(d[source], list) else d[source]
        tgt = tuple(d[target]) if isinstance(d[target], list) else d[target]
        if not multigraph:
            edgedata = {str(k): v for k, v in d.items() if k != source and k != target}
            graph.add_edge(src, tgt, **edgedata)
        else:
            ky = d.get(key, None)
            edgedata = {
                str(k): v
                for k, v in d.items()
                if k != source and k != target and k != key
            }
            graph.add_edge(src, tgt, ky, **edgedata)
    return graph
