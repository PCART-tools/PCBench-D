@wraps(pd.rolling_window)
def rolling_window(arg, window, **kwargs):
    if kwargs.pop('mean', True):
        return rolling_mean(arg, window, **kwargs)
    return rolling_sum(arg, window, **kwargs)
