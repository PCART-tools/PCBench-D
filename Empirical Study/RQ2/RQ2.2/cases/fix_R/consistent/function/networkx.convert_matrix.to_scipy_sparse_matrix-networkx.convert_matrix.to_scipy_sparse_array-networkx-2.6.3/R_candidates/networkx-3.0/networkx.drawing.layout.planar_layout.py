def planar_layout(G, scale=1, center=None, dim=2):
    """Position nodes without edge intersections.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G. If G is of type
        nx.PlanarEmbedding, the positions are selected accordingly.

    scale : number (default: 1)
        Scale factor for positions.

    center : array-like or None
        Coordinate pair around which to center the layout.

    dim : int
        Dimension of layout.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node

    Raises
    ------
    NetworkXException
        If G is not planar

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> pos = nx.planar_layout(G)
    """
    import numpy as np

    if dim != 2:
        raise ValueError("can only handle 2 dimensions")

    G, center = _process_params(G, center, dim)

    if len(G) == 0:
        return {}

    if isinstance(G, nx.PlanarEmbedding):
        embedding = G
    else:
        is_planar, embedding = nx.check_planarity(G)
        if not is_planar:
            raise nx.NetworkXException("G is not planar.")
    pos = nx.combinatorial_embedding_to_pos(embedding)
    node_list = list(embedding)
    pos = np.row_stack([pos[x] for x in node_list])
    pos = pos.astype(np.float64)
    pos = rescale_layout(pos, scale=scale) + center
    return dict(zip(node_list, pos))
