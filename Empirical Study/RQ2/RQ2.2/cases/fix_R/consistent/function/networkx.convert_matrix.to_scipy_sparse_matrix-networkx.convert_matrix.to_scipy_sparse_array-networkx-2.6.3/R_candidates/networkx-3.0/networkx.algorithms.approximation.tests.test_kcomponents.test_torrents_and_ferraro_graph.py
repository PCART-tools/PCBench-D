def test_torrents_and_ferraro_graph():
    G = torrents_and_ferraro_graph()
    _check_connectivity(G)
