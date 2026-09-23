def test_minimal_d_separator():
    # Case 1:
    # create a graph A -> B <- C
    # B -> D -> E;
    # B -> F;
    # G -> E;
    edge_list = [("A", "B"), ("C", "B"), ("B", "D"), ("D", "E"), ("B", "F"), ("G", "E")]
    G = nx.DiGraph(edge_list)
    assert not nx.d_separated(G, {"B"}, {"E"}, set())

    # minimal set of the corresponding graph
    # for B and E should be (D,)
    Zmin = nx.minimal_d_separator(G, "B", "E")

    # the minimal separating set should pass the test for minimality
    assert nx.is_minimal_d_separator(G, "B", "E", Zmin)
    assert Zmin == {"D"}

    # Case 2:
    # create a graph A -> B -> C
    # B -> D -> C;
    edge_list = [("A", "B"), ("B", "C"), ("B", "D"), ("D", "C")]
    G = nx.DiGraph(edge_list)
    assert not nx.d_separated(G, {"A"}, {"C"}, set())
    Zmin = nx.minimal_d_separator(G, "A", "C")

    # the minimal separating set should pass the test for minimality
    assert nx.is_minimal_d_separator(G, "A", "C", Zmin)
    assert Zmin == {"B"}
