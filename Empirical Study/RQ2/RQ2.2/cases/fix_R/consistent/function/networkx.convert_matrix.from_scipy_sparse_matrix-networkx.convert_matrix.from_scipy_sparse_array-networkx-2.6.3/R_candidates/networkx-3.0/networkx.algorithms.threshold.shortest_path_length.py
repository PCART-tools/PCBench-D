def shortest_path_length(creation_sequence, i):
    """
    Return the shortest path length from indicated node to
    every other node for the threshold graph with the given
    creation sequence.
    Node is indicated by index i in creation_sequence unless
    creation_sequence is labeled in which case, i is taken to
    be the label of the node.

    Paths lengths in threshold graphs are at most 2.
    Length to unreachable nodes is set to -1.
    """
    # Turn input sequence into a labeled creation sequence
    first = creation_sequence[0]
    if isinstance(first, str):  # creation sequence
        if isinstance(creation_sequence, list):
            cs = creation_sequence[:]
        else:
            cs = list(creation_sequence)
    elif isinstance(first, tuple):  # labeled creation sequence
        cs = [v[1] for v in creation_sequence]
        i = [v[0] for v in creation_sequence].index(i)
    elif isinstance(first, int):  # compact creation sequence
        cs = uncompact(creation_sequence)
    else:
        raise TypeError("Not a valid creation sequence type")

    # Compute
    N = len(cs)
    spl = [2] * N  # length 2 to every node
    spl[i] = 0  # except self which is 0
    # 1 for all d's to the right
    for j in range(i + 1, N):
        if cs[j] == "d":
            spl[j] = 1
    if cs[i] == "d":  # 1 for all nodes to the left
        for j in range(i):
            spl[j] = 1
    # and -1 for any trailing i to indicate unreachable
    for j in range(N - 1, 0, -1):
        if cs[j] == "d":
            break
        spl[j] = -1
    return spl
