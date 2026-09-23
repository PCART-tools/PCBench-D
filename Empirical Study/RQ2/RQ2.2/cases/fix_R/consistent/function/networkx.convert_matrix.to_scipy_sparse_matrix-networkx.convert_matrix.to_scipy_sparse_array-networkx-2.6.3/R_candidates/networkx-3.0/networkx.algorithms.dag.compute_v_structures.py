@not_implemented_for("undirected")
def compute_v_structures(G):
    """Iterate through the graph to compute all v-structures.

    V-structures are triples in the directed graph where
    two parent nodes point to the same child and the two parent nodes
    are not adjacent.

    Parameters
    ----------
    G : graph
        A networkx DiGraph.

    Returns
    -------
    vstructs : iterator of tuples
        The v structures within the graph. Each v structure is a 3-tuple with the
        parent, collider, and other parent.

    Notes
    -----
    https://en.wikipedia.org/wiki/Collider_(statistics)
    """
    for collider, preds in G.pred.items():
        for common_parents in combinations(preds, r=2):
            # ensure that the colliders are the same
            common_parents = sorted(common_parents)
            yield (common_parents[0], collider, common_parents[1])
