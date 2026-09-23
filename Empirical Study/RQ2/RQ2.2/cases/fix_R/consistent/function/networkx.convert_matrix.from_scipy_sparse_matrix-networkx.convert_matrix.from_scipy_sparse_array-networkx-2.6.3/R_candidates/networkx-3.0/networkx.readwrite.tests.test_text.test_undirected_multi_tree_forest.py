def test_undirected_multi_tree_forest():
    tree1 = nx.balanced_tree(r=2, h=2, create_using=nx.Graph)
    tree2 = nx.balanced_tree(r=2, h=2, create_using=nx.Graph)
    tree2 = nx.relabel_nodes(tree2, {n: n + len(tree1) for n in tree2.nodes})
    forest = nx.union(tree1, tree2)
    ret = nx.forest_str(forest, sources=[0, 7])
    print(ret)

    target = dedent(
        """
        ╟── 0
        ╎   ├── 1
        ╎   │   ├── 3
        ╎   │   └── 4
        ╎   └── 2
        ╎       ├── 5
        ╎       └── 6
        ╙── 7
            ├── 8
            │   ├── 10
            │   └── 11
            └── 9
                ├── 12
                └── 13
        """
    ).strip()
    assert ret == target

    ret = nx.forest_str(forest, sources=[0, 7], ascii_only=True)
    print(ret)

    target = dedent(
        """
        +-- 0
        :   |-- 1
        :   |   |-- 3
        :   |   L-- 4
        :   L-- 2
        :       |-- 5
        :       L-- 6
        +-- 7
            |-- 8
            |   |-- 10
            |   L-- 11
            L-- 9
                |-- 12
                L-- 13
        """
    ).strip()
    assert ret == target
