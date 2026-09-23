def cliques_containing_node(G, nodes=None, cliques=None):
    """Returns a list of cliques containing the given node.

    Returns a single list or list of lists depending on input nodes.
    Optional list of cliques can be input if already computed.
    """
    if cliques is None:
        cliques = list(find_cliques(G))

    if nodes is None:
        nodes = list(G.nodes())  # none, get entire graph

    if not isinstance(nodes, list):  # check for a list
        v = nodes
        # assume it is a single value
        vcliques = [c for c in cliques if v in c]
    else:
        vcliques = {}
        for v in nodes:
            vcliques[v] = [c for c in cliques if v in c]
    return vcliques
