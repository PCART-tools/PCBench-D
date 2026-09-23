def _possibly_downcast_to_dtype(result, dtype):
    """ try to cast to the specified dtype (e.g. convert back to bool/int
    or could be an astype of float64->float32
    """

    if np.isscalar(result):
        return result

    trans = lambda x: x
    if isinstance(dtype, compat.string_types):
        if dtype == 'infer':
            inferred_type = lib.infer_dtype(_ensure_object(result.ravel()))
            if inferred_type == 'boolean':
                dtype = 'bool'
            elif inferred_type == 'integer':
                dtype = 'int64'
            elif inferred_type == 'datetime64':
                dtype = 'datetime64[ns]'
            elif inferred_type == 'timedelta64':
                dtype = 'timedelta64[ns]'

            # try to upcast here
            elif inferred_type == 'floating':
                dtype = 'int64'
                if issubclass(result.dtype.type, np.number):
                    trans = lambda x: x.round()

            else:
                dtype = 'object'

    if isinstance(dtype, compat.string_types):
        dtype = np.dtype(dtype)

    try:

        # don't allow upcasts here (except if empty)
        if dtype.kind == result.dtype.kind:
            if result.dtype.itemsize <= dtype.itemsize and np.prod(result.shape):
                return result

        if issubclass(dtype.type, np.floating):
            return result.astype(dtype)
        elif dtype == np.bool_ or issubclass(dtype.type, np.integer):

            # if we don't have any elements, just astype it
            if not np.prod(result.shape):
                return trans(result).astype(dtype)

            # do a test on the first element, if it fails then we are done
            r = result.ravel()
            arr = np.array([r[0]])
            if not np.allclose(arr, trans(arr).astype(dtype)):
                return result

            # a comparable, e.g. a Decimal may slip in here
            elif not isinstance(r[0], (np.integer, np.floating, np.bool, int,
                                       float, bool)):
                return result

            if (issubclass(result.dtype.type, (np.object_, np.number)) and
                    notnull(result).all()):
                new_result = trans(result).astype(dtype)
                try:
                    if np.allclose(new_result, result):
                        return new_result
                except:

                    # comparison of an object dtype with a number type could
                    # hit here
                    if (new_result == result).all():
                        return new_result

        # a datetimelike
        elif dtype.kind in ['M','m'] and result.dtype.kind in ['i']:
            try:
                result = result.astype(dtype)
            except:
                pass

    except:
        pass

    return result
