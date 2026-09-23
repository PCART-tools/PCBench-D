def test_shortest_simple_paths_with_weight_fucntion():
    def cost(u, v, x):
        return 1

    G = nx.cycle_graph(7, create_using=nx.DiGraph())
    paths = nx.shortest_simple_paths(G, 0, 3, weight=cost)
    assert [path for path in paths] == [[0, 1, 2, 3]]
