def _convert_object_array(content, columns, coerce_float=False, dtype=None):
    if columns is None:
        columns = _default_index(len(content))
    else:
        if len(columns) != len(content):  # pragma: no cover
            # caller's responsibility to check for this...
            raise AssertionError('%d columns passed, passed data had %s '
                                 'columns' % (len(columns), len(content)))

    # provide soft conversion of object dtypes
    def convert(arr):
        if dtype != object and dtype != np.object:
            arr = lib.maybe_convert_objects(arr, try_float=coerce_float)
            arr = _possibly_cast_to_datetime(arr, dtype)
        return arr

    arrays = [convert(arr) for arr in content]

    return arrays, columns
