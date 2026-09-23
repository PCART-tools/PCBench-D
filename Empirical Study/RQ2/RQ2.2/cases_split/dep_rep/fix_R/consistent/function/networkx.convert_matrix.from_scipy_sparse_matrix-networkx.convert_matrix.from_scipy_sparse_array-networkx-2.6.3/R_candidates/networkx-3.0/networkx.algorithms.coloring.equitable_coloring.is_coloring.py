def is_coloring(G, coloring):
    """Determine if the coloring is a valid coloring for the graph G."""
    # Verify that the coloring is valid.
    for (s, d) in G.edges:
        if coloring[s] == coloring[d]:
            return False
    return True
