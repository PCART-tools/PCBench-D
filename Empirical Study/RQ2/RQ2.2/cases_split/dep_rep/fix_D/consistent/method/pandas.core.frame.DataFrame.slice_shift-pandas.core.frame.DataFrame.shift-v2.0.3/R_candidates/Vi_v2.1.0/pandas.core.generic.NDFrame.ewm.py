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
        axis: Axis | lib.NoDefault = lib.no_default,
        times: np.ndarray | DataFrame | Series | None = None,
        method: Literal["single", "table"] = "single",
    ) -> ExponentialMovingWindow:
        if axis is not lib.no_default:
            axis = self._get_axis_number(axis)
            name = "ewm"
            if axis == 1:
                warnings.warn(
                    f"Support for axis=1 in {type(self).__name__}.{name} is "
                    "deprecated and will be removed in a future version. "
                    f"Use obj.T.{name}(...) instead",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            else:
                warnings.warn(
                    f"The 'axis' keyword in {type(self).__name__}.{name} is "
                    "deprecated and will be removed in a future version. "
                    "Call the method without the axis keyword instead.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
        else:
            axis = 0

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
