@py_random_state(3)
def swap_d(cs, p_split=1.0, p_combine=1.0, seed=None):
    """
    Perform a "swap" operation on a threshold sequence.

    The swap preserves the number of nodes and edges
    in the graph for the given sequence.
    The resulting sequence is still a threshold sequence.

    Perform one split and one combine operation on the
    'd's of a creation sequence for a threshold graph.
    This operation maintains the number of nodes and edges
    in the graph, but shifts the edges from node to node
    maintaining the threshold quality of the graph.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    """
    # preprocess the creation sequence
    dlist = [i for (i, node_type) in enumerate(cs[1:-1]) if node_type == "d"]
    # split
    if seed.random() < p_split:
        choice = seed.choice(dlist)
        split_to = seed.choice(range(choice))
        flip_side = choice - split_to
        if split_to != flip_side and cs[split_to] == "i" and cs[flip_side] == "i":
            cs[choice] = "i"
            cs[split_to] = "d"
            cs[flip_side] = "d"
            dlist.remove(choice)
            # don't add or combine may reverse this action
            # dlist.extend([split_to,flip_side])
    #            print >>sys.stderr,"split at %s to %s and %s"%(choice,split_to,flip_side)
    # combine
    if seed.random() < p_combine and dlist:
        first_choice = seed.choice(dlist)
        second_choice = seed.choice(dlist)
        target = first_choice + second_choice
        if target >= len(cs) or cs[target] == "d" or first_choice == second_choice:
            return cs
        # OK to combine
        cs[first_choice] = "i"
        cs[second_choice] = "i"
        cs[target] = "d"
    #        print >>sys.stderr,"combine %s and %s to make %s."%(first_choice,second_choice,target)

    return cs
