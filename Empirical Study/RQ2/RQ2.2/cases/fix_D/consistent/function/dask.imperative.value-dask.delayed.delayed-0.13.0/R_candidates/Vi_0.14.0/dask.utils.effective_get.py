def effective_get(get=None, collection=None):
    """Get the effective get method used in a given situation"""
    collection_get = collection._default_get if collection else None
    return get or _globals.get('get') or collection_get
