def test_random_tree_using_generator():
    """Tests that creating a ramdom tree with a generator works"""
    G = nx.Graph()
    T = nx.random_tree(10, seed=1234, create_using=G)
    assert nx.is_tree(T)
