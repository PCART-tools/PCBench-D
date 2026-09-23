@pytest.mark.skipif(no_backends_for_leiden_partitions)
def test_partition_iterator():
    G = nx.path_graph(15)
    parts_iter = nx.community.leiden_partitions(G, seed=42)
    first_part = next(parts_iter)
    first_copy = [s.copy() for s in first_part]

    # check 1st part stays fixed even after 2nd iteration (like gh-5901 in louvain)
    assert first_copy[0] == first_part[0]
    second_part = next(parts_iter)
    assert first_copy[0] == first_part[0]
