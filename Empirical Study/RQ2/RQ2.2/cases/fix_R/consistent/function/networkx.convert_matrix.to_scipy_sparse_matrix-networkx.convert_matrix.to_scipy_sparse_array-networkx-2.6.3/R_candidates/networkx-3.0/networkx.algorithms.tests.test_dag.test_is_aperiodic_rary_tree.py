def test_is_aperiodic_rary_tree():
    G = nx.full_rary_tree(3, 27, create_using=nx.DiGraph())
    assert not nx.is_aperiodic(G)
