def _maybe_box(indexer, values, obj, key):

    # if we have multiples coming back, box em
    if isinstance(values, np.ndarray):
        return obj[indexer.get_loc(key)]

    # return the value
    return values
