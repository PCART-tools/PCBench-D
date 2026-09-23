def _build_agg_args_var(result_column, func, input_column):
    int_sum = _make_agg_id('sum', input_column)
    int_sum2 = _make_agg_id('sum2', input_column)
    int_count = _make_agg_id('count', input_column)

    return dict(
        chunk_funcs=[
            (int_sum, _apply_func_to_column,
             dict(column=input_column, func=M.sum)),
            (int_count, _apply_func_to_column,
             dict(column=input_column, func=M.count)),
            (int_sum2, _compute_sum_of_squares,
             dict(column=input_column)),
        ],
        aggregate_funcs=[
            (col, _apply_func_to_column, dict(column=col, func=M.sum))
            for col in (int_sum, int_count, int_sum2)
        ],
        finalizer=(result_column, _finalize_var,
                   dict(sum_column=int_sum, count_column=int_count,
                        sum2_column=int_sum2)),
    )
