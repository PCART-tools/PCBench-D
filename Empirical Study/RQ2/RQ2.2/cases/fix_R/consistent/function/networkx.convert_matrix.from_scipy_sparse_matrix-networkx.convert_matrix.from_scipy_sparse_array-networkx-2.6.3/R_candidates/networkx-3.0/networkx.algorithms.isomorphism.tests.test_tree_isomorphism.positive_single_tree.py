def positive_single_tree(t1):

    assert nx.is_tree(t1)

    nodes1 = [n for n in t1.nodes()]
    # get a random permutation of this
    nodes2 = nodes1.copy()
    random.shuffle(nodes2)

    # this is one isomorphism, however they may be multiple
    # so we don't necessarily get this one back
    someisomorphism = [(u, v) for (u, v) in zip(nodes1, nodes2)]

    # map from old to new
    map1to2 = {u: v for (u, v) in someisomorphism}

    # get the edges with the transformed names
    edges2 = [random_swap((map1to2[u], map1to2[v])) for (u, v) in t1.edges()]
    # randomly permute, to ensure we're not relying on edge order somehow
    random.shuffle(edges2)

    # so t2 is isomorphic to t1
    t2 = nx.Graph()
    t2.add_edges_from(edges2)

    # lets call our code to see if t1 and t2 are isomorphic
    isomorphism = tree_isomorphism(t1, t2)

    # make sure we got a correct solution
    # although not necessarily someisomorphism
    assert len(isomorphism) > 0
    assert check_isomorphism(t1, t2, isomorphism)
