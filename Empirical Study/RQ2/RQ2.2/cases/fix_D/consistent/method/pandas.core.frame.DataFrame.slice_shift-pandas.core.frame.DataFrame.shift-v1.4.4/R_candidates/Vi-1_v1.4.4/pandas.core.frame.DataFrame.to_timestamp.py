    def to_timestamp(
        self,
        freq: Frequency | None = None,
        how: str = "start",
        axis: Axis = 0,
        copy: bool = True,
    ) -> DataFrame:
        """
        Cast to DatetimeIndex of timestamps, at *beginning* of period.

        Parameters
        ----------
        freq : str, default frequency of PeriodIndex
            Desired frequency.
        how : {'s', 'e', 'start', 'end'}
            Convention for converting period to timestamp; start of period
            vs. end.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            The axis to convert (the index by default).
        copy : bool, default True
            If False then underlying input data is not copied.

        Returns
        -------
        DataFrame with DatetimeIndex
        """
        new_obj = self.copy(deep=copy)

        axis_name = self._get_axis_name(axis)
        old_ax = getattr(self, axis_name)
        if not isinstance(old_ax, PeriodIndex):
            raise TypeError(f"unsupported Type {type(old_ax).__name__}")

        new_ax = old_ax.to_timestamp(freq=freq, how=how)

        setattr(new_obj, axis_name, new_ax)
        return new_obj
