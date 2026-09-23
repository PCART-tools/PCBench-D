def test_isomorphism_iter1():
    # As described in:
    # http://groups.google.com/group/networkx-discuss/browse_thread/thread/2ff65c67f5e3b99f/d674544ebea359bb?fwc=1
    g1 = nx.DiGraph()
    g2 = nx.DiGraph()
    g3 = nx.DiGraph()
    g1.add_edge("A", "B")
    g1.add_edge("B", "C")
    g2.add_edge("Y", "Z")
    g3.add_edge("Z", "Y")
    gm12 = iso.DiGraphMatcher(g1, g2)
    gm13 = iso.DiGraphMatcher(g1, g3)
    x = list(gm12.subgraph_isomorphisms_iter())
    y = list(gm13.subgraph_isomorphisms_iter())
    assert {"A": "Y", "B": "Z"} in x
    assert {"B": "Y", "C": "Z"} in x
    assert {"A": "Z", "B": "Y"} in y
    assert {"B": "Z", "C": "Y"} in y
    assert len(x) == len(y)
    assert len(x) == 2
