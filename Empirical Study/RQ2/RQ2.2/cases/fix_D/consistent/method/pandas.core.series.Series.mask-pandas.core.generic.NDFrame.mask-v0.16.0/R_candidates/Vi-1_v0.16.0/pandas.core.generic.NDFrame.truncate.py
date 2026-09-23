    def truncate(self, before=None, after=None, axis=None, copy=True):
        """Truncates a sorted NDFrame before and/or after some particular
        dates.

        Parameters
        ----------
        before : date
            Truncate before date
        after : date
            Truncate after date
        axis : the truncation axis, defaults to the stat axis
        copy : boolean, default is True,
            return a copy of the truncated section

        Returns
        -------
        truncated : type of caller
        """

        if axis is None:
            axis = self._stat_axis_number
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        # if we have a date index, convert to dates, otherwise
        # treat like a slice
        if ax.is_all_dates:
            from pandas.tseries.tools import to_datetime
            before = to_datetime(before)
            after = to_datetime(after)

        if before is not None and after is not None:
            if before > after:
                raise ValueError('Truncate: %s must be after %s' %
                                 (after, before))

        slicer = [slice(None, None)] * self._AXIS_LEN
        slicer[axis] = slice(before, after)
        result = self.ix[tuple(slicer)]

        if isinstance(ax, MultiIndex):
            setattr(result, self._get_axis_name(axis),
                    ax.truncate(before, after))

        if copy:
            result = result.copy()

        return result
