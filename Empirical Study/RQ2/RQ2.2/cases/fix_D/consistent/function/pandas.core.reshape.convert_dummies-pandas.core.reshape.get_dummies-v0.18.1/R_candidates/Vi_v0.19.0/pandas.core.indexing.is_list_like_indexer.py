def is_list_like_indexer(key):
    # allow a list_like, but exclude NamedTuples which can be indexers
    return is_list_like(key) and not (isinstance(key, tuple) and
                                      type(key) is not tuple)
