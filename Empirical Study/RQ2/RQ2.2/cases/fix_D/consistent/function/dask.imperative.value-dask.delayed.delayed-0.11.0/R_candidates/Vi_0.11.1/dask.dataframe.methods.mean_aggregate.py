def mean_aggregate(s, n):
    try:
        return s / n
    except ZeroDivisionError:
        return np.nan
