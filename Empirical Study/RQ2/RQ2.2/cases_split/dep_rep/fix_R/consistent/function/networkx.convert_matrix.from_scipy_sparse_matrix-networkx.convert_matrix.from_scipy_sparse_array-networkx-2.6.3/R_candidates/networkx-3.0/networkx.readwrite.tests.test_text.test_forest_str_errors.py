def test_forest_str_errors():
    ugraph = nx.complete_graph(3, create_using=nx.Graph)

    with pytest.raises(nx.NetworkXNotImplemented):
        nx.forest_str(ugraph)

    dgraph = nx.complete_graph(3, create_using=nx.DiGraph)

    with pytest.raises(nx.NetworkXNotImplemented):
        nx.forest_str(dgraph)
