    def __init__(self, obj, window=None, min_periods=None, freq=None,
                 center=False, win_type=None, axis=0, on=None, closed=None,
                 **kwargs):

        if freq is not None:
            warnings.warn("The freq kw is deprecated and will be removed in a "
                          "future version. You can resample prior to passing "
                          "to a window function", FutureWarning, stacklevel=3)

        self.__dict__.update(kwargs)
        self.blocks = []
        self.obj = obj
        self.on = on
        self.closed = closed
        self.window = window
        self.min_periods = min_periods
        self.freq = freq
        self.center = center
        self.win_type = win_type
        self.axis = obj._get_axis_number(axis) if axis is not None else None
        self.validate()
