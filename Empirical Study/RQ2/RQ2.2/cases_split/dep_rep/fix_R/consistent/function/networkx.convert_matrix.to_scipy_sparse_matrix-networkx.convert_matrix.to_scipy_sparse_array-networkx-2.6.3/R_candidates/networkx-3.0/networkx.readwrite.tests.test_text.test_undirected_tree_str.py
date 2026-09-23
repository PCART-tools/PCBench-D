def test_undirected_tree_str():
    # Create a directed forest with labels
    graph = nx.balanced_tree(r=2, h=2, create_using=nx.Graph)

    # arbitrary starting point
    nx.forest_str(graph)

    node_target0 = dedent(
        """
        ╙── 0
            ├── 1
            │   ├── 3
            │   └── 4
            └── 2
                ├── 5
                └── 6
        """
    ).strip()

    # defined starting point
    ret = nx.forest_str(graph, sources=[0])
    print(ret)
    assert ret == node_target0

    # defined starting point
    node_target2 = dedent(
        """
        ╙── 2
            ├── 0
            │   └── 1
            │       ├── 3
            │       └── 4
            ├── 5
            └── 6
        """
    ).strip()
    ret = nx.forest_str(graph, sources=[2])
    print(ret)
    assert ret == node_target2
