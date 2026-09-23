def _build_agg_args_simple(result_column, func, input_column, impl_pair):
    intermediate = _make_agg_id(func, input_column)
    chunk_impl, agg_impl = impl_pair

    return dict(
        chunk_funcs=[(intermediate, _apply_func_to_column,
                     dict(column=input_column, func=chunk_impl))],
        aggregate_funcs=[(intermediate, _apply_func_to_column,
                         dict(column=intermediate, func=agg_impl))],
        finalizer=(result_column, operator.itemgetter(intermediate), dict()),
    )
