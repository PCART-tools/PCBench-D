def _get_consensus_names(indexes):

    # find the non-none names, need to tupleify to make
    # the set hashable, then reverse on return
    consensus_names = set([
        tuple(i.names) for i in indexes if all(n is not None for n in i.names)
    ])
    if len(consensus_names) == 1:
        return list(list(consensus_names)[0])
    return [None] * indexes[0].nlevels
