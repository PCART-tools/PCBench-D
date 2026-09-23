def _find_proxy(*objects_to_search):
    """
    Recursively search a data structure for a Proxy() and return it,
    return None if not found.
    """
    proxy = None

    def find_proxy(x):
        nonlocal proxy
        if isinstance(x, Proxy):
            proxy = x

    map_aggregate(objects_to_search, find_proxy)
    return proxy
