def concat(dfs, axis=0, join='outer'):
    """ Concatenate caring empty Series """

    # can be removed after pandas 0.18.1 or later
    # see https://github.com/pandas-dev/pandas/pull/12846
    if PANDAS_VERSION >= '0.18.1':
        return pd.concat(dfs, axis=axis, join=join)

    # Concat with empty Series with axis=1 will not affect to the
    # result. Special handling is needed in each partition
    if axis == 1:
        # becahse dfs is a generator, once convert to list
        dfs = list(dfs)

        if join == 'outer':
            # outer concat should keep all empty Series

            # input must include one non-empty data at least
            # because of the alignment
            first = [df for df in dfs if len(df) > 0][0]

            def _pad(base, fillby):
                if isinstance(base, pd.Series) and len(base) == 0:
                    # use aligned index to keep index for outer concat
                    return pd.Series([np.nan] * len(fillby),
                                     index=fillby.index, name=base.name)
                else:
                    return base

            dfs = [_pad(df, first) for df in dfs]
        else:
            # inner concat should result in empty if any input is empty
            if any(len(df) == 0 for df in dfs):
                dfs = [pd.DataFrame(columns=df.columns)
                       if isinstance(df, pd.DataFrame) else
                       pd.Series(name=df.name) for df in dfs]

    return pd.concat(dfs, axis=axis, join=join)
