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

        # we need a timelike key here
        if idx.is_all_dates:
            try:
                return idx._get_string_slice(key)
            except:
                return None

    return None
