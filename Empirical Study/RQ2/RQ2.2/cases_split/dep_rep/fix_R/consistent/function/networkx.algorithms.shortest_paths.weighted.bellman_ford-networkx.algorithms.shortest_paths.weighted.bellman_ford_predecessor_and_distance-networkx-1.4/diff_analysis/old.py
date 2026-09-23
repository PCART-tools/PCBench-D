def bellman_ford(G, source, weight = 'weight'):
    """Compute shortest path lengths and predecessors on shortest paths 
    in weighted graphs.

    The algorithm has a running time of O(mn) where n is the number of nodes 
    and n is the number of edges.

    Parameters
    ----------
    G : NetworkX graph
       The algorithm works for all types of graphs, including directed
       graphs and multigraphs.

    source: node label
       Starting node for path

    weight: string, optional       
       Edge data key corresponding to the edge weight

    Returns
    -------
    pred,dist : dictionaries
       Returns two dictionaries representing a list of predecessors 
       of a node and the distance from the source to each node. The
       dictionaries are keyed by target node label.

    Raises
    ------
    NetworkXUnbounded
       If the (di)graph contains a negative cost (di)cycle, the
       algorithm raises an exception to indicate the presence of the
       negative cost (di)cycle.

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
    >>> G = nx.cycle_graph(5)
    >>> G[1][2]['weight'] = -7
    >>> assert_raises(nx.NetworkXUnbounded, nx.bellman_ford, G, 0)
   
    Notes
    -----
    The dictionaries returned only have keys for nodes reachable from
    the source.

    In the case where the (di)graph is not connected, if a component
    not containing the source contains a negative cost (di)cycle, it
    will not be detected.

    """

    if not G.is_directed():
        directed = False
    else:
        directed = True

    dist = {source: 0}
    pred = {source: None}

    if G.number_of_nodes() == 1:
       return pred, dist
    
    def process_edge(u, v, weight):
        # Just a helper function for the main algorithm below.
        if dist.get(u) is not None:
            if dist.get(v) is None or dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                pred[v] = u
                return False
        return True

    for i in range(G.number_of_nodes()):
        feasible = True
        for u, v in G.edges():
            if G.is_multigraph():
                edata = min([eattr.get(weight, 1)
                             for eattr in G[u][v].values()])
            else:
                edata = G[u][v].get(weight, 1)
            if not process_edge(u, v, edata):
                feasible = False
            if not directed:
                if not (v, u) in G.edges():
                    if not process_edge(v, u, edata):
                        feasible = False
        if feasible:
            break

    if i + 1 == G.number_of_nodes():
        raise nx.NetworkXUnbounded("Negative cost cycle detected.")
    return pred, dist
