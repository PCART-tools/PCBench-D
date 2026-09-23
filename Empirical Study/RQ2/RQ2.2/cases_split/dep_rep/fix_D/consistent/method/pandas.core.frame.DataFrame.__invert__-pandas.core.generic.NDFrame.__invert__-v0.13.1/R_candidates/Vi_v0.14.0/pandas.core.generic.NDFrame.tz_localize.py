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
            if len(ax) > 0:
                ax_name = self._get_axis_name(axis)
                raise TypeError('%s is not a valid DatetimeIndex or PeriodIndex' %
                                ax_name)
            else:
                ax = DatetimeIndex([],tz=tz)
        else:
            ax = ax.tz_localize(tz, infer_dst=infer_dst)

        result = self._constructor(self._data, copy=copy)
        result.set_axis(axis,ax)
        return result.__finalize__(self)
