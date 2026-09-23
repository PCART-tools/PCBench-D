def test_seed_argument():
    G = nx.barbell_graph(3, 0)
    C = kernighan_lin_bisection(G, seed=1)
    assert_partition_equal(C, [{0, 1, 2}, {3, 4, 5}])
