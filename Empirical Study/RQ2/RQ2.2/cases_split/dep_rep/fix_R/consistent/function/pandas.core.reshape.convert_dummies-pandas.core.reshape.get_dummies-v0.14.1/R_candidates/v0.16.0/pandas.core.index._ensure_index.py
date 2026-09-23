def _ensure_index(index_like, copy=False):
    if isinstance(index_like, Index):
        if copy:
            index_like = index_like.copy()
        return index_like
    if hasattr(index_like, 'name'):
        return Index(index_like, name=index_like.name, copy=copy)

    # must check for exactly list here because of strict type
    # check in clean_index_list
    if isinstance(index_like, list):
        if type(index_like) != list:
            index_like = list(index_like)
        # 2200 ?
        converted, all_arrays = lib.clean_index_list(index_like)

        if len(converted) > 0 and all_arrays:
            return MultiIndex.from_arrays(converted)
        else:
            index_like = converted
    else:
       # clean_index_list does the equivalent of copying
       # so only need to do this if not list instance
        if copy:
            from copy import copy
            index_like = copy(index_like)

    return Index(index_like)
