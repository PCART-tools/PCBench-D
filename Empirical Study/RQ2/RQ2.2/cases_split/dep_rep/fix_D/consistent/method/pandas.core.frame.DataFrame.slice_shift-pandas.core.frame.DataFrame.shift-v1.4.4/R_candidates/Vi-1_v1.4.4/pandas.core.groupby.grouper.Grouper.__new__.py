    def __new__(cls, *args, **kwargs):
        if kwargs.get("freq") is not None:
            from pandas.core.resample import TimeGrouper

            _check_deprecated_resample_kwargs(kwargs, origin=cls)
            cls = TimeGrouper
        return super().__new__(cls)
