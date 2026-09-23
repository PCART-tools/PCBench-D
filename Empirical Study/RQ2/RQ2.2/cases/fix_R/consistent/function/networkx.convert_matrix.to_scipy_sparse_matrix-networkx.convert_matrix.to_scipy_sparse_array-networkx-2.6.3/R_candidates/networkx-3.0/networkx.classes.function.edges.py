def edges(G, nbunch=None):
    """Returns an edge view of edges incident to nodes in nbunch.

    Return all edges if nbunch is unspecified or nbunch=None.

    For digraphs, edges=out_edges
    """
    return G.edges(nbunch)
