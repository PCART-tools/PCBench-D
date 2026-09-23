    def __new__(cls, *args, **kwargs):
        from pandas.core.resample import TimeGrouper
        import warnings
        warnings.warn("pd.TimeGrouper is deprecated and will be removed; "
                      "Please use pd.Grouper(freq=...)",
                      FutureWarning, stacklevel=2)
        return TimeGrouper(*args, **kwargs)
