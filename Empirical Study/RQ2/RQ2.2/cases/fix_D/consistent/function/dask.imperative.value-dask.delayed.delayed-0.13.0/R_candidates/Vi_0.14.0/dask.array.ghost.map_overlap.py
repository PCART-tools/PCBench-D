def map_overlap(x, func, depth, boundary=None, trim=True, **kwargs):
    depth2 = coerce_depth(x.ndim, depth)
    boundary2 = coerce_boundary(x.ndim, boundary)

    g = ghost(x, depth=depth2, boundary=boundary2)
    g2 = g.map_blocks(func, **kwargs)
    if trim:
        g3 = add_dummy_padding(g2, depth2, boundary2)
        return trim_internal(g3, depth2)
    else:
        return g2
