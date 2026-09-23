    def tz_convert(self, tz, axis=0, level=None, copy=True):
        """
        Convert tz-aware axis to target time zone.

        Parameters
        ----------
        tz : string or pytz.timezone object
        axis : the axis to convert
        level : int, str, default None
            If axis ia a MultiIndex, convert a specific level. Otherwise
            must be None
        copy : boolean, default True
            Also make a copy of the underlying data

        Returns
        -------

        Raises
        ------
        TypeError
            If the axis is tz-naive.
        """
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        def _tz_convert(ax, tz):
            if not hasattr(ax, 'tz_convert'):
                if len(ax) > 0:
                    ax_name = self._get_axis_name(axis)
                    raise TypeError('%s is not a valid DatetimeIndex or '
                                    'PeriodIndex' % ax_name)
                else:
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
                raise ValueError("The level {0} is not valid".format(level))
            ax = _tz_convert(ax, tz)

        result = self._constructor(self._data, copy=copy)
        result = result.set_axis(ax, axis=axis, inplace=False)
        return result.__finalize__(self)
