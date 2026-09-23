def estimate_graph_size(old_chunks, new_chunks):
    """ Estimate the graph size during a rechunk computation.
    """
    # Estimate the number of intermediate blocks that will be produced
    # (we don't use intersect_chunks() which is much more expensive)
    crossed_size = reduce(mul, (len(oc) + len(nc)
                                for oc, nc in zip(old_chunks, new_chunks)))
    return crossed_size
