def test_multigraph():
    G = nx.cycle_graph(4)
    M = nx.MultiGraph(G.edges())
    M.add_edges_from(G.edges())
    M.remove_edge(1, 2)
    for labels in permutations(range(4)):
        mapping = dict(zip(M, labels))
        A, B = kernighan_lin_bisection(nx.relabel_nodes(M, mapping), seed=0)
        assert_partition_equal(
            [A, B], [{mapping[0], mapping[1]}, {mapping[2], mapping[3]}]
        )
