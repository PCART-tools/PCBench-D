    def __new__(cls, *args, **kwargs):
        if kwargs.get('freq') is not None:
            from pandas.core.resample import TimeGrouper
            cls = TimeGrouper
        return super(Grouper, cls).__new__(cls)
