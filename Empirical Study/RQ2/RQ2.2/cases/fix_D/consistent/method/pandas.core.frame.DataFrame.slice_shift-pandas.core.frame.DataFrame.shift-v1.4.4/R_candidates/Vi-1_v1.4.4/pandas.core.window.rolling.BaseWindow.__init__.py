    def __init__(
        self,
        obj: NDFrame,
        window=None,
        min_periods: int | None = None,
        center: bool = False,
        win_type: str | None = None,
        axis: Axis = 0,
        on: str | Index | None = None,
        closed: str | None = None,
        method: str = "single",
        *,
        selection=None,
    ):
        self.obj = obj
        self.on = on
        self.closed = closed
        self.window = window
        self.min_periods = min_periods
        self.center = center
        # TODO(2.0): Change this back to self.win_type once deprecation is enforced
        self._win_type = win_type
        self.axis = obj._get_axis_number(axis) if axis is not None else None
        self.method = method
        self._win_freq_i8 = None
        if self.on is None:
            if self.axis == 0:
                self._on = self.obj.index
            else:
                # i.e. self.axis == 1
                self._on = self.obj.columns
        elif isinstance(self.on, Index):
            self._on = self.on
        elif isinstance(self.obj, ABCDataFrame) and self.on in self.obj.columns:
            self._on = Index(self.obj[self.on])
        else:
            raise ValueError(
                f"invalid on specified as {self.on}, "
                "must be a column (of DataFrame), an Index or None"
            )

        self._selection = selection
        self._validate()
