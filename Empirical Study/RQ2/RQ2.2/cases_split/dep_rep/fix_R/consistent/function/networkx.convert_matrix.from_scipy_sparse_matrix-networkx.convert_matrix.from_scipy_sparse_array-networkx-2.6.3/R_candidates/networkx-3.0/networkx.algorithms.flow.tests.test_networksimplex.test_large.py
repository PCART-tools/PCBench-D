def test_large():
    fname = os.path.join(os.path.dirname(__file__), "netgen-2.gpickle.bz2")
    with bz2.BZ2File(fname, "rb") as f:
        G = pickle.load(f)
    flowCost, flowDict = nx.network_simplex(G)
    assert 6749969302 == flowCost
    assert 6749969302 == nx.cost_of_flow(G, flowDict)
