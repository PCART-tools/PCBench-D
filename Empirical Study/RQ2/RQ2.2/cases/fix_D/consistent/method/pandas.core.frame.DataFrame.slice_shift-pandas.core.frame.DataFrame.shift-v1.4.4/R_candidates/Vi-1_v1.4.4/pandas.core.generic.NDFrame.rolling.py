    @final
    @doc(Rolling)
    def rolling(
        self,
        window: int | timedelta | BaseOffset | BaseIndexer,
        min_periods: int | None = None,
        center: bool_t = False,
        win_type: str | None = None,
        on: str | None = None,
        axis: Axis = 0,
        closed: str | None = None,
        method: str = "single",
    ):
        axis = self._get_axis_number(axis)

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
            method=method,
        )
