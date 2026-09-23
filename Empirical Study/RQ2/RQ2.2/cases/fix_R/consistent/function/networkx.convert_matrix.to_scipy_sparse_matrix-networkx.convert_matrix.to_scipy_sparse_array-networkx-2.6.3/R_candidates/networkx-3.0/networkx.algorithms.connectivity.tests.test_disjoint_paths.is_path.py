def is_path(G, path):
    return all(v in G[u] for u, v in pairwise(path))
