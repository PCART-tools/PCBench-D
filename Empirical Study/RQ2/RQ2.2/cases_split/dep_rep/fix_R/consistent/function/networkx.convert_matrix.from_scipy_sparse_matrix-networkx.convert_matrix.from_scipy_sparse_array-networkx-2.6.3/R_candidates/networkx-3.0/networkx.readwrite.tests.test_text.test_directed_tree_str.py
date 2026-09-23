def test_directed_tree_str():
    # Create a directed forest with labels
    graph = nx.balanced_tree(r=2, h=2, create_using=nx.DiGraph)
    for node in graph.nodes:
        graph.nodes[node]["label"] = "node_" + chr(ord("a") + node)

    node_target = dedent(
        """
        ╙── 0
            ├─╼ 1
            │   ├─╼ 3
            │   └─╼ 4
            └─╼ 2
                ├─╼ 5
                └─╼ 6
        """
    ).strip()

    label_target = dedent(
        """
        ╙── node_a
            ├─╼ node_b
            │   ├─╼ node_d
            │   └─╼ node_e
            └─╼ node_c
                ├─╼ node_f
                └─╼ node_g
        """
    ).strip()

    # Basic node case
    ret = nx.forest_str(graph, with_labels=False)
    print(ret)
    assert ret == node_target

    # Basic label case
    ret = nx.forest_str(graph, with_labels=True)
    print(ret)
    assert ret == label_target

    # Custom write function case
    lines = []
    ret = nx.forest_str(graph, write=lines.append, with_labels=False)
    assert ret is None
    assert lines == node_target.split("\n")

    # Smoke test to ensure passing the print function works. To properly test
    # this case we would need to capture stdout. (for potential reference
    # implementation see :class:`ubelt.util_stream.CaptureStdout`)
    ret = nx.forest_str(graph, write=print)
    assert ret is None
