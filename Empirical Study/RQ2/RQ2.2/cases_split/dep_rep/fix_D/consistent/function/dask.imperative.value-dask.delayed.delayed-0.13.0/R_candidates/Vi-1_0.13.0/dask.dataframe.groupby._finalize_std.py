def _finalize_std(df, count_column, sum_column, sum2_column, ddof=1):
    result = _finalize_var(df, count_column, sum_column, sum2_column, ddof)
    return np.sqrt(result)
