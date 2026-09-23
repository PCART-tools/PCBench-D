def maximum_spanning_arborescence(
    G, attr="weight", default=1, preserve_attrs=False, partition=None
):
    ed = Edmonds(G)
    B = ed.find_optimum(
        attr,
        default,
        kind="max",
        style="arborescence",
        preserve_attrs=preserve_attrs,
        partition=partition,
    )
    if not is_arborescence(B):
        msg = "No maximum spanning arborescence in G."
        raise nx.exception.NetworkXException(msg)
    return B
