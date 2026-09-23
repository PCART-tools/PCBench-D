def assign_levels(G, root):
    level = {}
    level[root] = 0
    for (v1, v2) in nx.bfs_edges(G, root):
        level[v2] = level[v1] + 1

    return level
