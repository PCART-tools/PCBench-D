def _four_cycles(G):
    cycles = 0
    for v in G:
        for u, w in itertools.combinations(G[v], 2):
            cycles += len((set(G[u]) & set(G[w])) - {v})
    return cycles / 4
