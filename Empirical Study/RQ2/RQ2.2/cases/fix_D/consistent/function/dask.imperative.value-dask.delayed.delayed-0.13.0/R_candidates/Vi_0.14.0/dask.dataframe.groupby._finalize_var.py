def _finalize_var(df, count_column, sum_column, sum2_column, ddof=1):
    n = df[count_column]
    x = df[sum_column]
    x2 = df[sum2_column]

    result = x2 - x ** 2 / n
    div = (n - ddof)
    div[div < 0] = 0
    result /= div
    result[(n - ddof) == 0] = np.nan

    return result
