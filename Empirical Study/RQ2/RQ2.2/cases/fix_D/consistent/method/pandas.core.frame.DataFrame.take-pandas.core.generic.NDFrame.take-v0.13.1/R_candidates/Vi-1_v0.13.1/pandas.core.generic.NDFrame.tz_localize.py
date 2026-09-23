    def tz_localize(self, tz, axis=0, copy=True, infer_dst=False):
        """
        Localize tz-naive TimeSeries to target time zone

        Parameters
        ----------
        tz : string or pytz.timezone object
        copy : boolean, default True
            Also make a copy of the underlying data
        infer_dst : boolean, default False
            Attempt to infer fall dst-transition times based on order

        Returns
        -------
        """
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        if not hasattr(ax, 'tz_localize'):
            ax_name = self._get_axis_name(axis)
            raise TypeError('%s is not a valid DatetimeIndex or PeriodIndex' %
                            ax_name)

        new_data = self._data
        if copy:
            new_data = new_data.copy()

        new_obj = self._constructor(new_data)
        new_ax = ax.tz_localize(tz, infer_dst=infer_dst)

        if axis == 0:
            new_obj._set_axis(1, new_ax)
        elif axis == 1:
            new_obj._set_axis(0, new_ax)
            self._clear_item_cache()

        return new_obj.__finalize__(self)
