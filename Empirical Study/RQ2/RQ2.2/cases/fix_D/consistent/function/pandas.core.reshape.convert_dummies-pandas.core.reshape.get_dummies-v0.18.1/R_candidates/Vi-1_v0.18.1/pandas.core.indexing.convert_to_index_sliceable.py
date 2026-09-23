def convert_to_index_sliceable(obj, key):
    """if we are index sliceable, then return my slicer, otherwise return None
    """
    idx = obj.index
    if isinstance(key, slice):
        return idx._convert_slice_indexer(key, kind='getitem')

    elif isinstance(key, compat.string_types):

        # we are an actual column
        if key in obj._data.items:
            return None

        # We might have a datetimelike string that we can translate to a
        # slice here via partial string indexing
        if idx.is_all_dates:
            try:
                return idx._get_string_slice(key)
            except (KeyError, ValueError, NotImplementedError):
                return None

    return None
