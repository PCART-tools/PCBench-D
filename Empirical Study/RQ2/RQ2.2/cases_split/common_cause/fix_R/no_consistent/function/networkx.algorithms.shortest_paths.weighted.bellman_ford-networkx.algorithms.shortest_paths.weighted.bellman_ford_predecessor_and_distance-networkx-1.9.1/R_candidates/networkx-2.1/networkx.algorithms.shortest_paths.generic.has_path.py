def has_path(G, source, target):
    """Return *True* if *G* has a path from *source* to *target*.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path

    target : node
       Ending node for path
    """
    try:
        sp = nx.shortest_path(G, source, target)
    except nx.NetworkXNoPath:
        return False
    return True
