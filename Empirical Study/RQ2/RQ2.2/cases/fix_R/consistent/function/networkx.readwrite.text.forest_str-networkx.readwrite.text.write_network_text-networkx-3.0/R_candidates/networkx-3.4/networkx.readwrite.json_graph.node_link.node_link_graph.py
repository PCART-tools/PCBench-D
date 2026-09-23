@nx._dispatchable(graphs=None, returns_graph=True)
def node_link_graph(
    data,
    directed=False,
    multigraph=True,
    *,
    source="source",
    target="target",
    name="id",
    key="key",
    edges=None,
    nodes="nodes",
    link=None,
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

    source : string
        A string that provides the 'source' attribute name for storing NetworkX-internal graph data.
    target : string
        A string that provides the 'target' attribute name for storing NetworkX-internal graph data.
    name : string
        A string that provides the 'name' attribute name for storing NetworkX-internal graph data.
    key : string
        A string that provides the 'key' attribute name for storing NetworkX-internal graph data.
    edges : string
        A string that provides the 'edges' attribute name for storing NetworkX-internal graph data.
    nodes : string
        A string that provides the 'nodes' attribute name for storing NetworkX-internal graph data.
    link : string
        .. deprecated:: 3.4

           The `link` argument is deprecated and will be removed in version `3.6`.
           Use the `edges` keyword instead.

        A string that provides the 'edges' attribute name for storing NetworkX-internal graph data.

    Returns
    -------
    G : NetworkX graph
        A NetworkX graph object

    Examples
    --------

    Create data in node-link format by converting a graph.

    >>> from pprint import pprint
    >>> G = nx.Graph([("A", "B")])
    >>> data = nx.node_link_data(G, edges="edges")
    >>> pprint(data)
    {'directed': False,
     'edges': [{'source': 'A', 'target': 'B'}],
     'graph': {},
     'multigraph': False,
     'nodes': [{'id': 'A'}, {'id': 'B'}]}

    Revert data in node-link format to a graph.

    >>> H = nx.node_link_graph(data, edges="edges")
    >>> print(H.edges)
    [('A', 'B')]

    To serialize and deserialize a graph with JSON,

    >>> import json
    >>> d = json.dumps(nx.node_link_data(G, edges="edges"))
    >>> H = nx.node_link_graph(json.loads(d), edges="edges")
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
    # TODO: Remove between the lines when `link` deprecation expires
    # -------------------------------------------------------------
    if link is not None:
        warnings.warn(
            "Keyword argument 'link' is deprecated; use 'edges' instead",
            DeprecationWarning,
            stacklevel=2,
        )
        if edges is not None:
            raise ValueError(
                "Both 'edges' and 'link' are specified. Use 'edges', 'link' will be remove in a future release"
            )
        else:
            edges = link
    else:
        if edges is None:
            warnings.warn(
                (
                    '\nThe default value will be changed to `edges="edges" in NetworkX 3.6.\n\n'
                    "To make this warning go away, explicitly set the edges kwarg, e.g.:\n\n"
                    '  nx.node_link_graph(data, edges="links") to preserve current behavior, or\n'
                    '  nx.node_link_graph(data, edges="edges") for forward compatibility.'
                ),
                FutureWarning,
            )
            edges = "links"
    # -------------------------------------------------------------

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
    for d in data[nodes]:
        node = _to_tuple(d.get(name, next(c)))
        nodedata = {str(k): v for k, v in d.items() if k != name}
        graph.add_node(node, **nodedata)
    for d in data[edges]:
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
