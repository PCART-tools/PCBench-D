def triangles(creation_sequence):
    """
    Compute number of triangles in the threshold graph with the
    given creation sequence.
    """
    # shortcut algorithm that doesn't require computing number
    # of triangles at each node.
    cs = creation_sequence  # alias
    dr = cs.count("d")  # number of d's in sequence
    ntri = dr * (dr - 1) * (dr - 2) / 6  # number of triangles in clique of nd d's
    # now add dr choose 2 triangles for every 'i' in sequence where
    # dr is the number of d's to the right of the current i
    for i, typ in enumerate(cs):
        if typ == "i":
            ntri += dr * (dr - 1) / 2
        else:
            dr -= 1
    return ntri
