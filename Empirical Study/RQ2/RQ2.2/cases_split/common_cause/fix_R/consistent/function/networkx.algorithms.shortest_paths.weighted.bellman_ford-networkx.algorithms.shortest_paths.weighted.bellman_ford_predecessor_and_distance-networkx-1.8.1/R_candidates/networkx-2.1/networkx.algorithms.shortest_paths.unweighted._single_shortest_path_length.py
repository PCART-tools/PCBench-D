def _single_shortest_path_length(adj, firstlevel, cutoff):
    """Yields (node, level) in a breadth first search

    Shortest Path Length helper function
    Parameters
    ----------
        adj : dict
            Adjacency dict or view
        firstlevel : dict
            starting nodes, e.g. {source: 1} or {target: 1}
        cutoff : int or float
            level at which we stop the process
    """
    seen = {}                  # level (number of hops) when seen in BFS
    level = 0                  # the current level
    nextlevel = firstlevel     # dict of nodes to check at next level

    while nextlevel and cutoff >= level:
        thislevel = nextlevel  # advance to next level
        nextlevel = {}         # and start a new list (fringe)
        for v in thislevel:
            if v not in seen:
                seen[v] = level  # set the level of vertex v
                nextlevel.update(adj[v])  # add neighbors of v
                yield (v, level)
        level += 1
    del seen
