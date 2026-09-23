    @final
    @doc(klass=_shared_doc_kwargs["klass"])
    def tz_convert(
        self: NDFrameT, tz, axis: Axis = 0, level=None, copy: bool_t | None = None
    ) -> NDFrameT:
        """
        Convert tz-aware axis to target time zone.

        Parameters
        ----------
        tz : str or tzinfo object or None
            Target time zone. Passing ``None`` will convert to
            UTC and remove the timezone information.
        axis : {{0 or 'index', 1 or 'columns'}}, default 0
            The axis to convert
        level : int, str, default None
            If axis is a MultiIndex, convert a specific level. Otherwise
            must be None.
        copy : bool, default True
            Also make a copy of the underlying data.

        Returns
        -------
        {klass}
            Object with time zone converted axis.

        Raises
        ------
        TypeError
            If the axis is tz-naive.

        Examples
        --------
        Change to another time zone:

        >>> s = pd.Series(
        ...     [1],
        ...     index=pd.DatetimeIndex(['2018-09-15 01:30:00+02:00']),
        ... )
        >>> s.tz_convert('Asia/Shanghai')
        2018-09-15 07:30:00+08:00    1
        dtype: int64

        Pass None to convert to UTC and get a tz-naive index:

        >>> s = pd.Series([1],
        ...     index=pd.DatetimeIndex(['2018-09-15 01:30:00+02:00']))
        >>> s.tz_convert(None)
        2018-09-14 23:30:00    1
        dtype: int64
        """
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        def _tz_convert(ax, tz):
            if not hasattr(ax, "tz_convert"):
                if len(ax) > 0:
                    ax_name = self._get_axis_name(axis)
                    raise TypeError(
                        f"{ax_name} is not a valid DatetimeIndex or PeriodIndex"
                    )
                ax = DatetimeIndex([], tz=tz)
            else:
                ax = ax.tz_convert(tz)
            return ax

        # if a level is given it must be a MultiIndex level or
        # equivalent to the axis name
        if isinstance(ax, MultiIndex):
            level = ax._get_level_number(level)
            new_level = _tz_convert(ax.levels[level], tz)
            ax = ax.set_levels(new_level, level=level)
        else:
            if level not in (None, 0, ax.name):
                raise ValueError(f"The level {level} is not valid")
            ax = _tz_convert(ax, tz)

        result = self.copy(deep=copy and not using_copy_on_write())
        result = result.set_axis(ax, axis=axis, copy=False)
        return result.__finalize__(self, method="tz_convert")
