    @deprecate_kwarg(old_arg_name='infer_dst', new_arg_name='ambiguous',
                     mapping={True: 'infer', False: 'raise'})
    def tz_localize(self, tz, axis=0, level=None, copy=True,
                    ambiguous='raise'):
        """
        Localize tz-naive TimeSeries to target time zone

        Parameters
        ----------
        tz : string or pytz.timezone object
        axis : the axis to localize
        level : int, str, default None
            If axis ia a MultiIndex, localize a specific level. Otherwise
            must be None
        copy : boolean, default True
            Also make a copy of the underlying data
        ambiguous : 'infer', bool-ndarray, 'NaT', default 'raise'
            - 'infer' will attempt to infer fall dst-transition hours based on order
            - bool-ndarray where True signifies a DST time, False designates
              a non-DST time (note that this flag is only applicable for ambiguous times)
            - 'NaT' will return NaT where there are ambiguous times
            - 'raise' will raise an AmbiguousTimeError if there are ambiguous times
        infer_dst : boolean, default False (DEPRECATED)
            Attempt to infer fall dst-transition hours based on order

        Returns
        -------
        """
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        def _tz_localize(ax, tz, ambiguous):
            if not hasattr(ax, 'tz_localize'):
                if len(ax) > 0:
                    ax_name = self._get_axis_name(axis)
                    raise TypeError('%s is not a valid DatetimeIndex or PeriodIndex' %
                                    ax_name)
                else:
                    ax = DatetimeIndex([],tz=tz)
            else:
                ax = ax.tz_localize(tz, ambiguous=ambiguous)
            return ax

        # if a level is given it must be a MultiIndex level or
        # equivalent to the axis name
        if isinstance(ax, MultiIndex):
            level = ax._get_level_number(level)
            new_level = _tz_localize(ax.levels[level], tz, ambiguous)
            ax = ax.set_levels(new_level, level=level)
        else:
            if level not in (None, 0, ax.name):
                raise ValueError("The level {0} is not valid".format(level))
            ax =  _tz_localize(ax, tz, ambiguous)

        result = self._constructor(self._data, copy=copy)
        result.set_axis(axis,ax)
        return result.__finalize__(self)
