def maximum_branching(
    G, attr="weight", default=1, preserve_attrs=False, partition=None
):
    ed = Edmonds(G)
    B = ed.find_optimum(
        attr,
        default,
        kind="max",
        style="branching",
        preserve_attrs=preserve_attrs,
        partition=partition,
    )
    return B
