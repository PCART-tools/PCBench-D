def _get_dummies_1d(data, prefix, prefix_sep='_', dummy_na=False,
                    sparse=False, drop_first=False):
    # Series avoids inconsistent NaN handling
    codes, levels = _factorize_from_iterable(Series(data))

    def get_empty_Frame(data, sparse):
        if isinstance(data, Series):
            index = data.index
        else:
            index = np.arange(len(data))
        if not sparse:
            return DataFrame(index=index)
        else:
            return SparseDataFrame(index=index)

    # if all NaN
    if not dummy_na and len(levels) == 0:
        return get_empty_Frame(data, sparse)

    codes = codes.copy()
    if dummy_na:
        codes[codes == -1] = len(levels)
        levels = np.append(levels, np.nan)

    # if dummy_na, we just fake a nan level. drop_first will drop it again
    if drop_first and len(levels) == 1:
        return get_empty_Frame(data, sparse)

    number_of_cols = len(levels)

    if prefix is not None:
        dummy_cols = ['%s%s%s' % (prefix, prefix_sep, v) for v in levels]
    else:
        dummy_cols = levels

    if isinstance(data, Series):
        index = data.index
    else:
        index = None

    if sparse:
        sparse_series = {}
        N = len(data)
        sp_indices = [[] for _ in range(len(dummy_cols))]
        for ndx, code in enumerate(codes):
            if code == -1:
                # Blank entries if not dummy_na and code == -1, #GH4446
                continue
            sp_indices[code].append(ndx)

        if drop_first:
            # remove first categorical level to avoid perfect collinearity
            # GH12042
            sp_indices = sp_indices[1:]
            dummy_cols = dummy_cols[1:]
        for col, ixs in zip(dummy_cols, sp_indices):
            sarr = SparseArray(np.ones(len(ixs), dtype=np.uint8),
                               sparse_index=IntIndex(N, ixs), fill_value=0,
                               dtype=np.uint8)
            sparse_series[col] = SparseSeries(data=sarr, index=index)

        out = SparseDataFrame(sparse_series, index=index, columns=dummy_cols,
                              dtype=np.uint8)
        return out

    else:
        dummy_mat = np.eye(number_of_cols, dtype=np.uint8).take(codes, axis=0)

        if not dummy_na:
            # reset NaN GH4446
            dummy_mat[codes == -1] = 0

        if drop_first:
            # remove first GH12042
            dummy_mat = dummy_mat[:, 1:]
            dummy_cols = dummy_cols[1:]
        return DataFrame(dummy_mat, index=index, columns=dummy_cols)
