def dfs_labeled_edges(G, source=None, depth_limit=None):
    """Iterate over edges in a depth-first-search (DFS) labeled by type.

    Parameters
    ----------
    G : NetworkX graph

    source : node, optional
       Specify starting node for depth-first search and return edges in
       the component reachable from source.

    depth_limit : int, optional (default=len(G))
       Specify the maximum search depth.

    Returns
    -------
    edges: generator
       A generator of triples of the form (*u*, *v*, *d*), where (*u*,
       *v*) is the edge being explored in the depth-first search and *d*
       is one of the strings 'forward', 'nontree', 'reverse', or 'reverse-depth_limit'.
       A 'forward' edge is one in which *u* has been visited but *v* has
       not. A 'nontree' edge is one in which both *u* and *v* have been
       visited but the edge is not in the DFS tree. A 'reverse' edge is
       one in which both *u* and *v* have been visited and the edge is in
       the DFS tree. When the `depth_limit` is reached via a 'forward' edge,
       a 'reverse' edge is immediately generated rather than the subtree
       being explored. To indicate this flavor of 'reverse' edge, the string
       yielded is 'reverse-depth_limit'.

    Examples
    --------

    The labels reveal the complete transcript of the depth-first search
    algorithm in more detail than, for example, :func:`dfs_edges`::

        >>> from pprint import pprint
        >>>
        >>> G = nx.DiGraph([(0, 1), (1, 2), (2, 1)])
        >>> pprint(list(nx.dfs_labeled_edges(G, source=0)))
        [(0, 0, 'forward'),
         (0, 1, 'forward'),
         (1, 2, 'forward'),
         (2, 1, 'nontree'),
         (1, 2, 'reverse'),
         (0, 1, 'reverse'),
         (0, 0, 'reverse')]

    Notes
    -----
    If a source is not specified then a source is chosen arbitrarily and
    repeatedly until all components in the graph are searched.

    The implementation of this function is adapted from David Eppstein's
    depth-first search function in `PADS`_, with modifications
    to allow depth limits based on the Wikipedia article
    "`Depth-limited search`_".

    .. _PADS: http://www.ics.uci.edu/~eppstein/PADS
    .. _Depth-limited search: https://en.wikipedia.org/wiki/Depth-limited_search

    See Also
    --------
    dfs_edges
    dfs_preorder_nodes
    dfs_postorder_nodes
    """
    # Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
    # by D. Eppstein, July 2004.
    if source is None:
        # edges for all components
        nodes = G
    else:
        # edges for components with source
        nodes = [source]
    visited = set()
    if depth_limit is None:
        depth_limit = len(G)
    for start in nodes:
        if start in visited:
            continue
        yield start, start, "forward"
        visited.add(start)
        stack = [(start, depth_limit, iter(G[start]))]
        while stack:
            parent, depth_now, children = stack[-1]
            try:
                child = next(children)
                if child in visited:
                    yield parent, child, "nontree"
                else:
                    yield parent, child, "forward"
                    visited.add(child)
                    if depth_now > 1:
                        stack.append((child, depth_now - 1, iter(G[child])))
                    else:
                        yield parent, child, "reverse-depth_limit"
            except StopIteration:
                stack.pop()
                if stack:
                    yield stack[-1][0], parent, "reverse"
        yield start, start, "reverse"
