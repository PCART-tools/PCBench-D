def pivot_count(df, index, columns, values):
    # we cannot determine dtype until concatenationg all partitions.
    # make dtype deterministic, always coerce to np.float64
    return pd.pivot_table(df, index=index, columns=columns,
                          values=values, aggfunc='count').astype(np.float64)
