def process_val_weights(vals_and_weights, npartitions, dtype_info):
    """Calculate final approximate percentiles given weighted vals

    ``vals_and_weights`` is assumed to be sorted.  We take a cumulative
    sum of the weights, which makes them percentile-like (their scale is
    [0, N] instead of [0, 100]).  Next we find the divisions to create
    partitions of approximately equal size.

    It is possible for adjacent values of the result to be the same.  Since
    these determine the divisions of the new partitions, some partitions
    may be empty.  This can happen if we under-sample the data, or if there
    aren't enough unique values in the column.  Increasing ``upsample``
    keyword argument in ``df.set_index`` may help.
    """
    vals, weights = vals_and_weights
    vals = np.array(vals)
    weights = np.array(weights)
    dtype, info = dtype_info

    # We want to create exactly `npartition` number of groups of `vals` that
    # are approximately the same weight and non-empty if possible.  We use a
    # simple approach (more accurate algorithms exist):
    # 1. Remove all the values with weights larger than the relative
    #    percentile width from consideration (these are `jumbo`s)
    # 2. Calculate percentiles with "interpolation=left" of percentile-like
    #    weights of the remaining values.  These are guaranteed to be unique.
    # 3. Concatenate the values from (1) and (2), sort, and return.
    #
    # We assume that all values are unique, which happens in the previous
    # step `merge_and_compress_summaries`.

    if len(vals) == npartitions + 1:
        rv = vals
    elif len(vals) < npartitions + 1:
        # The data is under-sampled
        if np.issubdtype(vals.dtype, np.number):
            # Interpolate extra divisions
            q_weights = np.cumsum(weights)
            q_target = np.linspace(q_weights[0], q_weights[-1], npartitions + 1)
            rv = np.interp(q_target, q_weights, vals)
        else:
            # Distribute the empty partitions
            duplicated_index = np.linspace(
                0, len(vals) - 1, npartitions - len(vals) + 1, dtype=int
            )
            duplicated_vals = vals[duplicated_index]
            rv = np.concatenate([vals, duplicated_vals])
            rv.sort()
    else:
        target_weight = weights.sum() / npartitions
        jumbo_mask = weights >= target_weight
        jumbo_vals = vals[jumbo_mask]

        trimmed_vals = vals[~jumbo_mask]
        trimmed_weights = weights[~jumbo_mask]
        trimmed_npartitions = npartitions - len(jumbo_vals)

        # percentile-like, but scaled by weights
        q_weights = np.cumsum(trimmed_weights)
        q_target = np.linspace(0, q_weights[-1], trimmed_npartitions + 1)

        left = np.searchsorted(q_weights, q_target, side='left')
        right = np.searchsorted(q_weights, q_target, side='right') - 1
        # stay inbounds
        np.maximum(right, 0, right)
        lower = np.minimum(left, right)
        trimmed = trimmed_vals[lower]

        rv = np.concatenate([trimmed, jumbo_vals])
        rv.sort()

    if str(dtype) == 'category':
        rv = pd.Categorical.from_codes(rv, info[0], info[1])
    elif 'datetime64' in str(dtype):
        rv = pd.DatetimeIndex(rv, dtype=dtype)
    elif rv.dtype != dtype:
        rv = rv.astype(dtype)
    return rv
