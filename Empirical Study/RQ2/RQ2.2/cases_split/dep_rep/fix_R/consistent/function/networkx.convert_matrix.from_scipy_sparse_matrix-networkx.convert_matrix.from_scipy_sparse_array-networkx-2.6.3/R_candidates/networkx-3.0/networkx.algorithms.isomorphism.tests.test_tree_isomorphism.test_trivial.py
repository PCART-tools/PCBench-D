def test_trivial():

    print("trivial test")

    # back to an undirected graph
    t1 = nx.Graph()
    t1.add_node("a")
    root1 = "a"

    t2 = nx.Graph()
    t2.add_node("n")
    root2 = "n"

    isomorphism = rooted_tree_isomorphism(t1, root1, t2, root2)

    assert isomorphism == [("a", "n")]

    assert check_isomorphism(t1, t2, isomorphism)
