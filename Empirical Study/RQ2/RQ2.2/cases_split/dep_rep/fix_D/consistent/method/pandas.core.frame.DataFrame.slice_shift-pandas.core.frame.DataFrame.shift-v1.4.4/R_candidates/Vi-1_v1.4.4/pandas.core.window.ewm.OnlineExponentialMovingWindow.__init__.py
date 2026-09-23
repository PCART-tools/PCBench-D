    def __init__(
        self,
        obj: NDFrame,
        com: float | None = None,
        span: float | None = None,
        halflife: float | TimedeltaConvertibleTypes | None = None,
        alpha: float | None = None,
        min_periods: int | None = 0,
        adjust: bool = True,
        ignore_na: bool = False,
        axis: Axis = 0,
        times: str | np.ndarray | NDFrame | None = None,
        engine: str = "numba",
        engine_kwargs: dict[str, bool] | None = None,
        *,
        selection=None,
    ):
        if times is not None:
            raise NotImplementedError(
                "times is not implemented with online operations."
            )
        super().__init__(
            obj=obj,
            com=com,
            span=span,
            halflife=halflife,
            alpha=alpha,
            min_periods=min_periods,
            adjust=adjust,
            ignore_na=ignore_na,
            axis=axis,
            times=times,
            selection=selection,
        )
        self._mean = EWMMeanState(
            self._com, self.adjust, self.ignore_na, self.axis, obj.shape
        )
        if maybe_use_numba(engine):
            self.engine = engine
            self.engine_kwargs = engine_kwargs
        else:
            raise ValueError("'numba' is the only supported engine")
