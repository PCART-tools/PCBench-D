def _clear_cache(G):
    """Clear the cache of a graph (currently stores converted graphs).

    Caching is controlled via ``nx.config.cache_converted_graphs`` configuration.
    """
    if cache := getattr(G, "__networkx_cache__", None):
        cache.clear()
