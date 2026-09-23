def _build_agg_args_mean(result_column, func, input_column):
    int_sum = _make_agg_id('sum', input_column)
    int_count = _make_agg_id('count', input_column)

    return dict(
        chunk_funcs=[
            (int_sum, _apply_func_to_column,
             dict(column=input_column, func=M.sum)),
            (int_count, _apply_func_to_column,
             dict(column=input_column, func=M.count)),
        ],
        aggregate_funcs=[
            (col, _apply_func_to_column, dict(column=col, func=M.sum))
            for col in (int_sum, int_count)
        ],
        finalizer=(result_column, _finalize_mean,
                   dict(sum_column=int_sum, count_column=int_count)),
    )
