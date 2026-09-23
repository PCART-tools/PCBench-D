def _finalize_mean(df, sum_column, count_column):
    return df[sum_column] / df[count_column]
