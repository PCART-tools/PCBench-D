def test_normalized():
    with pytest.raises(nx.NetworkXError):
        sm = nx.s_metric(nx.Graph(), normalized=True)
