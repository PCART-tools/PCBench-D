    @final
    @doc(Rolling)
    def rolling(
        self,
        window: int | dt.timedelta | str | BaseOffset | BaseIndexer,
        min_periods: int | None = None,
        center: bool_t = False,
        win_type: str | None = None,
        on: str | None = None,
        axis: Axis | lib.NoDefault = lib.no_default,
        closed: IntervalClosedType | None = None,
        step: int | None = None,
        method: str = "single",
    ) -> Window | Rolling:
        if axis is not lib.no_default:
            axis = self._get_axis_number(axis)
            name = "rolling"
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

        if win_type is not None:
            return Window(
                self,
                window=window,
                min_periods=min_periods,
                center=center,
                win_type=win_type,
                on=on,
                axis=axis,
                closed=closed,
                step=step,
                method=method,
            )

        return Rolling(
            self,
            window=window,
            min_periods=min_periods,
            center=center,
            win_type=win_type,
            on=on,
            axis=axis,
            closed=closed,
            step=step,
            method=method,
        )
