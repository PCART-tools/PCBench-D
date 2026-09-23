def shortest_path(creation_sequence, u, v):
    """
    Find the shortest path between u and v in a
    threshold graph G with the given creation_sequence.

    For an unlabeled creation_sequence, the vertices
    u and v must be integers in (0,len(sequence)) referring
    to the position of the desired vertices in the sequence.

    For a labeled creation_sequence, u and v are labels of veritices.

    Use cs=creation_sequence(degree_sequence,with_labels=True)
    to convert a degree sequence to a creation sequence.

    Returns a list of vertices from u to v.
    Example: if they are neighbors, it returns [u,v]
    """
    # Turn input sequence into a labeled creation sequence
    first = creation_sequence[0]
    if isinstance(first, str):  # creation sequence
        cs = [(i, creation_sequence[i]) for i in range(len(creation_sequence))]
    elif isinstance(first, tuple):  # labeled creation sequence
        cs = creation_sequence[:]
    elif isinstance(first, int):  # compact creation sequence
        ci = uncompact(creation_sequence)
        cs = [(i, ci[i]) for i in range(len(ci))]
    else:
        raise TypeError("Not a valid creation sequence type")

    verts = [s[0] for s in cs]
    if v not in verts:
        raise ValueError(f"Vertex {v} not in graph from creation_sequence")
    if u not in verts:
        raise ValueError(f"Vertex {u} not in graph from creation_sequence")
    # Done checking
    if u == v:
        return [u]

    uindex = verts.index(u)
    vindex = verts.index(v)
    bigind = max(uindex, vindex)
    if cs[bigind][1] == "d":
        return [u, v]
    # must be that cs[bigind][1]=='i'
    cs = cs[bigind:]
    while cs:
        vert = cs.pop()
        if vert[1] == "d":
            return [u, vert[0], v]
    # All after u are type 'i' so no connection
    return -1
