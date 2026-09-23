def _homogenize(data, index, dtype=None):
    from pandas.core.series import _sanitize_array

    oindex = None
    homogenized = []

    for v in data:
        if isinstance(v, Series):
            if dtype is not None:
                v = v.astype(dtype)
            if v.index is not index:
                # Forces alignment. No need to copy data since we
                # are putting it into an ndarray later
                v = v.reindex(index, copy=False)
        else:
            if isinstance(v, dict):
                if oindex is None:
                    oindex = index.astype('O')
                if type(v) == dict:
                    # fast cython method
                    v = lib.fast_multiget(v, oindex.values, default=NA)
                else:
                    v = lib.map_infer(oindex.values, v.get)

            v = _sanitize_array(v, index, dtype=dtype, copy=False,
                                raise_cast_failure=False)

        homogenized.append(v)

    return homogenized
