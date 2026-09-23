def test_articulation_points():
    Ggen = _generate_no_biconnected()
    for i in range(1):  # change 1 to 3 or more for more realizations.
        G = next(Ggen)
        articulation_points = list({a} for a in nx.articulation_points(G))
        for cut in nx.all_node_cuts(G):
            assert cut in articulation_points
