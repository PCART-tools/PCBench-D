def _flex_binary_moment(arg1, arg2, f, pairwise=False):
    from pandas import Series, DataFrame, Panel
    if not (isinstance(arg1, (np.ndarray, Series, DataFrame)) and
            isinstance(arg2, (np.ndarray, Series, DataFrame))):
        raise TypeError("arguments to moment function must be of type "
                        "np.ndarray/Series/DataFrame")

    if (isinstance(arg1, (np.ndarray, Series)) and
            isinstance(arg2, (np.ndarray, Series))):
        X, Y = _prep_binary(arg1, arg2)
        return f(X, Y)

    elif isinstance(arg1, DataFrame):

        def dataframe_from_int_dict(data, frame_template):
            result = DataFrame(data, index=frame_template.index)
            if len(result.columns) > 0:
                result.columns = frame_template.columns[result.columns]
            return result

        results = {}
        if isinstance(arg2, DataFrame):
            if pairwise is False:
                if arg1 is arg2:
                    # special case in order to handle duplicate column names
                    for i, col in enumerate(arg1.columns):
                        results[i] = f(arg1.iloc[:, i], arg2.iloc[:, i])
                    return dataframe_from_int_dict(results, arg1)
                else:
                    if not arg1.columns.is_unique:
                        raise ValueError("'arg1' columns are not unique")
                    if not arg2.columns.is_unique:
                        raise ValueError("'arg2' columns are not unique")
                    X, Y = arg1.align(arg2, join='outer')
                    X = X + 0 * Y
                    Y = Y + 0 * X
                    res_columns = arg1.columns.union(arg2.columns)
                    for col in res_columns:
                        if col in X and col in Y:
                            results[col] = f(X[col], Y[col])
                    return DataFrame(results, index=X.index,
                                     columns=res_columns)
            elif pairwise is True:
                results = defaultdict(dict)
                for i, k1 in enumerate(arg1.columns):
                    for j, k2 in enumerate(arg2.columns):
                        if j < i and arg2 is arg1:
                            # Symmetric case
                            results[i][j] = results[j][i]
                        else:
                            results[i][j] = f(*_prep_binary(arg1.iloc[:, i],
                                                            arg2.iloc[:, j]))
                p = Panel.from_dict(results).swapaxes('items', 'major')
                if len(p.major_axis) > 0:
                    p.major_axis = arg1.columns[p.major_axis]
                if len(p.minor_axis) > 0:
                    p.minor_axis = arg2.columns[p.minor_axis]
                return p
            else:
                raise ValueError("'pairwise' is not True/False")
        else:
            results = {}
            for i, col in enumerate(arg1.columns):
                results[i] = f(*_prep_binary(arg1.iloc[:, i], arg2))
            return dataframe_from_int_dict(results, arg1)

    else:
        return _flex_binary_moment(arg2, arg1, f)
