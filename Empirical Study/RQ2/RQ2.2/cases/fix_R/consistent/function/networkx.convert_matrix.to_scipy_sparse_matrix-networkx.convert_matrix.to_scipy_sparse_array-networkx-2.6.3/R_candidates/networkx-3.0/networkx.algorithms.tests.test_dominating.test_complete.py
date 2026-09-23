def test_complete():
    """In complete graphs each node is a dominating set.
    Thus the dominating set has to be of cardinality 1.
    """
    K4 = nx.complete_graph(4)
    assert len(nx.dominating_set(K4)) == 1
    K5 = nx.complete_graph(5)
    assert len(nx.dominating_set(K5)) == 1
