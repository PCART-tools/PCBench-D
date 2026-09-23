def wrap_rolling(func, method_name):
    """Create a chunked version of a pandas.rolling_* function"""
    @wraps(func)
    def rolling(arg, window, *args, **kwargs):
        # pd.rolling_* functions are deprecated
        warnings.warn(("DeprecationWarning: dd.rolling_{0} is deprecated and "
                       "will be removed in a future version, replace with "
                       "df.rolling(...).{0}(...)").format(method_name))

        rolling_kwargs = {}
        method_kwargs = {}
        for k, v in kwargs.items():
            if k in {'min_periods', 'center', 'win_type', 'axis', 'freq'}:
                rolling_kwargs[k] = v
            else:
                method_kwargs[k] = v
        rolling = arg.rolling(window, **rolling_kwargs)
        return getattr(rolling, method_name)(*args, **method_kwargs)
    return rolling
