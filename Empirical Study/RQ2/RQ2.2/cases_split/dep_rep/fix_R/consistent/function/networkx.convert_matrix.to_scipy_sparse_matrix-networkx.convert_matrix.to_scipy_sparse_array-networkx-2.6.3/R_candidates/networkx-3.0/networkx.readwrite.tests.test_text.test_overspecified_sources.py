def test_overspecified_sources():
    """
    When sources are directly specified, we wont be able to determine when we
    are in the last component, so there will always be a trailing, leftmost
    pipe.
    """
    graph = nx.disjoint_union_all(
        [
            nx.balanced_tree(r=2, h=1, create_using=nx.DiGraph),
            nx.balanced_tree(r=1, h=2, create_using=nx.DiGraph),
            nx.balanced_tree(r=2, h=1, create_using=nx.DiGraph),
        ]
    )

    # defined starting point
    target1 = dedent(
        """
        ╟── 0
        ╎   ├─╼ 1
        ╎   └─╼ 2
        ╟── 3
        ╎   └─╼ 4
        ╎       └─╼ 5
        ╟── 6
        ╎   ├─╼ 7
        ╎   └─╼ 8
        """
    ).strip()

    target2 = dedent(
        """
        ╟── 0
        ╎   ├─╼ 1
        ╎   └─╼ 2
        ╟── 3
        ╎   └─╼ 4
        ╎       └─╼ 5
        ╙── 6
            ├─╼ 7
            └─╼ 8
        """
    ).strip()

    lines = []
    nx.forest_str(graph, write=lines.append, sources=graph.nodes)
    got1 = chr(10).join(lines)
    print("got1: ")
    print(got1)

    lines = []
    nx.forest_str(graph, write=lines.append)
    got2 = chr(10).join(lines)
    print("got2: ")
    print(got2)

    assert got1 == target1
    assert got2 == target2
