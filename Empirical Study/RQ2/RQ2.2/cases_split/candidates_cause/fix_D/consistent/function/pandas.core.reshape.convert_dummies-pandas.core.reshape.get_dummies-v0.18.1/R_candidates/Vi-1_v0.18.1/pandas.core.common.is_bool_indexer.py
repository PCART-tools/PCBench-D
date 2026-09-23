def is_bool_indexer(key):
    if isinstance(key, (gt.ABCSeries, np.ndarray)):
        if key.dtype == np.object_:
            key = np.asarray(_values_from_object(key))

            if not lib.is_bool_array(key):
                if isnull(key).any():
                    raise ValueError('cannot index with vector containing '
                                     'NA / NaN values')
                return False
            return True
        elif key.dtype == np.bool_:
            return True
    elif isinstance(key, list):
        try:
            arr = np.asarray(key)
            return arr.dtype == np.bool_ and len(arr) == len(key)
        except TypeError:  # pragma: no cover
            return False

    return False
