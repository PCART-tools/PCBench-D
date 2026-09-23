    def tz_convert(self, tz, axis=0, copy=True):
        """
        Convert the axis to target time zone. If it is time zone naive, it
        will be localized to the passed time zone.

        Parameters
        ----------
        tz : string or pytz.timezone object
        copy : boolean, default True
            Also make a copy of the underlying data

        Returns
        -------
        """
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        if not hasattr(ax, 'tz_convert'):
            if len(ax) > 0:
                ax_name = self._get_axis_name(axis)
                raise TypeError('%s is not a valid DatetimeIndex or PeriodIndex' %
                                ax_name)
            else:
                ax = DatetimeIndex([],tz=tz)
        else:
            ax = ax.tz_convert(tz)

        result = self._constructor(self._data, copy=copy)
        result.set_axis(axis,ax)
        return result.__finalize__(self)
