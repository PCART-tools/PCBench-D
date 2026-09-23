    def __init__(
        self,
        obj,
        window=None,
        min_periods: Optional[int] = None,
        center: Optional[bool] = False,
        win_type: Optional[str] = None,
        axis: Axis = 0,
        on: Optional[Union[str, Index]] = None,
        closed: Optional[str] = None,
        **kwargs,
    ):

        self.__dict__.update(kwargs)
        self.obj = obj
        self.on = on
        self.closed = closed
        self.window = window
        self.min_periods = min_periods
        self.center = center
        self.win_type = win_type
        self.win_freq = None
        self.axis = obj._get_axis_number(axis) if axis is not None else None
        self.validate()
        self._numba_func_cache: Dict[Optional[str], Callable] = dict()
