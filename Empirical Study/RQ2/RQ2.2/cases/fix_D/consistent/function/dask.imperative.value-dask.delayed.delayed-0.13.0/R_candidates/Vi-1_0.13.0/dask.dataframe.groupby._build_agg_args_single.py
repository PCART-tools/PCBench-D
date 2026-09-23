def _build_agg_args_single(result_column, func, input_column):
    simple_impl = {
        'sum': (M.sum, M.sum),
        'min': (M.min, M.min),
        'max': (M.max, M.max),
        'count': (M.count, M.sum),
        'size': (M.size, M.sum),
    }

    if func in simple_impl.keys():
        return _build_agg_args_simple(result_column, func, input_column,
                                      simple_impl[func])

    elif func == 'var':
        return _build_agg_args_var(result_column, func, input_column)

    elif func == 'std':
        return _build_agg_args_std(result_column, func, input_column)

    elif func == 'mean':
        return _build_agg_args_mean(result_column, func, input_column)

    else:
        raise ValueError("unknown aggregate {}".format(func))
