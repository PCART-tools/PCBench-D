    @final
    @doc(ExponentialMovingWindow)
    def ewm(
        self,
        com: float | None = None,
        span: float | None = None,
        halflife: float | TimedeltaConvertibleTypes | None = None,
        alpha: float | None = None,
        min_periods: int | None = 0,
        adjust: bool_t = True,
        ignore_na: bool_t = False,
        axis: Axis = 0,
        times: np.ndarray | DataFrame | Series | None = None,
        method: str = "single",
    ) -> ExponentialMovingWindow:
        axis = self._get_axis_number(axis)
        return ExponentialMovingWindow(
            self,
            com=com,
            span=span,
            halflife=halflife,
            alpha=alpha,
            min_periods=min_periods,
            adjust=adjust,
            ignore_na=ignore_na,
            axis=axis,
            times=times,
            method=method,
        )
