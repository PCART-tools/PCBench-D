def bellman_ford(G, source, weight='weight'):
    """DEPRECATED: Replaced by bellman_ford_predecessor_and_distance().

    """
    msg = "Function bellman_ford() is deprecated and will be removed" \
        "in 2.1, use bellman_ford_predecessor_and_distance() instead."
    _warnings.warn(msg, DeprecationWarning)

    return bellman_ford_predecessor_and_distance(G, source, weight=weight)
