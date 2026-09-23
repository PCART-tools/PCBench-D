def test_empty_graph():
    assert nx.forest_str(nx.DiGraph()) == "╙"
    assert nx.forest_str(nx.Graph()) == "╙"
