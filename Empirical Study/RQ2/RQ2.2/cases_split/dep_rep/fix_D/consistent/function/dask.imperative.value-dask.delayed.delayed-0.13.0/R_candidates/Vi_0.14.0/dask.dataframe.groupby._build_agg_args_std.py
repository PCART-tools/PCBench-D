def _build_agg_args_std(result_column, func, input_column):
    impls = _build_agg_args_var(result_column, func, input_column)

    result_column, _, kwargs = impls['finalizer']
    impls['finalizer'] = (result_column, _finalize_std, kwargs)

    return impls
