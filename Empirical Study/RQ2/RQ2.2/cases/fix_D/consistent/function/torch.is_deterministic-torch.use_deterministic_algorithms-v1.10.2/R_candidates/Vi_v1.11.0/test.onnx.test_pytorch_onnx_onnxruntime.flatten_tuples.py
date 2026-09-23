def flatten_tuples(elem):
    tup = []
    for t in elem:
        if isinstance(t, (tuple)):
            tup += flatten_tuples(t)
        else:
            tup += [t]
    return tup
