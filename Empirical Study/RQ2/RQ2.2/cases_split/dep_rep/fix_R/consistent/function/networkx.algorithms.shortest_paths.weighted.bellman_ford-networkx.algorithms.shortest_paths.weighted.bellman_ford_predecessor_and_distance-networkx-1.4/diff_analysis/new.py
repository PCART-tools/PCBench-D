def bellman_ford(G, source, weight = 'weight'):
    """Compute shortest path lengths and predecessors on shortest paths 
    in weighted graphs.

    The algorithm has a running time of O(mn) where n is the number of 
    nodes and m is the number of edges.  It is slower than Dijkstra but
    can handle negative edge weights.

    Parameters
    ----------
    G : NetworkX graph
       The algorithm works for all types of graphs, including directed
       graphs and multigraphs.

    source: node label
       Starting node for path

    weight: string, optional (default='weight')
       Edge data key corresponding to the edge weight

    Returns
    -------
    pred, dist : dictionaries
       Returns two dictionaries keyed by node to predecessor in the 
       path and to the distance from the source respectively.

    Raises
    ------
    NetworkXUnbounded
       If the (di)graph contains a negative cost (di)cycle, the
       algorithm raises an exception to indicate the presence of the
       negative cost (di)cycle.  Note: any negative weight edge in an
       undirected graph is a negative cost cycle.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.path_graph(5, create_using = nx.DiGraph())
    >>> pred, dist = nx.bellman_ford(G, 0)
    >>> pred
    {0: None, 1: 0, 2: 1, 3: 2, 4: 3}
    >>> dist
    {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

    >>> from nose.tools import assert_raises
    >>> G = nx.cycle_graph(5, create_using = nx.DiGraph())
    >>> G[1][2]['weight'] = -7
    >>> assert_raises(nx.NetworkXUnbounded, nx.bellman_ford, G, 0)
   
    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    The dictionaries returned only have keys for nodes reachable from
    the source.

    In the case where the (di)graph is not connected, if a component
    not containing the source contains a negative cost (di)cycle, it
    will not be detected.

    """
    if source not in G:
        raise KeyError("Node %s is not found in the graph"%source)
    numb_nodes = len(G)

    dist = {source: 0}
    pred = {source: None}

    if numb_nodes == 1:
       return pred, dist
    
    if G.is_multigraph():
        def get_weight(edge_dict):
            return min([eattr.get(weight,1) for eattr in edge_dict.values()])
    else:
        def get_weight(edge_dict):
            return edge_dict.get(weight,1)

    for i in range(numb_nodes):
        no_changes=True
        # Only need edges from nodes in dist b/c all others have dist==inf
        for u, dist_u in list(dist.items()): # get all edges from nodes in dist
            for v, edict in G[u].items():  # double loop handles undirected too
                dist_v = dist_u + get_weight(edict)
                if v not in dist or dist[v] > dist_v:
                    dist[v] = dist_v
                    pred[v] = u
                    no_changes = False
        if no_changes:
            break
    else:
        raise nx.NetworkXUnbounded("Negative cost cycle detected.")
    return pred, dist
