    @deprecate_kwarg(old_arg_name='infer_dst', new_arg_name='ambiguous',
                     mapping={True: 'infer', False: 'raise'})
    def tz_localize(self, tz, ambiguous='raise', errors='raise'):
        """
        Localize tz-naive DatetimeIndex to given time zone (using
        pytz/dateutil), or remove timezone from tz-aware DatetimeIndex

        Parameters
        ----------
        tz : string, pytz.timezone, dateutil.tz.tzfile or None
            Time zone for time. Corresponding timestamps would be converted to
            time zone of the TimeSeries.
            None will remove timezone holding local time.
        ambiguous : 'infer', bool-ndarray, 'NaT', default 'raise'
            - 'infer' will attempt to infer fall dst-transition hours based on
              order
            - bool-ndarray where True signifies a DST time, False signifies a
              non-DST time (note that this flag is only applicable for
              ambiguous times)
            - 'NaT' will return NaT where there are ambiguous times
            - 'raise' will raise an AmbiguousTimeError if there are ambiguous
              times
        errors : 'raise', 'coerce', default 'raise'
            - 'raise' will raise a NonExistentTimeError if a timestamp is not
               valid in the specified timezone (e.g. due to a transition from
               or to DST time)
            - 'coerce' will return NaT if the timestamp can not be converted
              into the specified timezone

            .. versionadded:: 0.19.0

        infer_dst : boolean, default False
            .. deprecated:: 0.15.0
               Attempt to infer fall dst-transition hours based on order

        Returns
        -------
        localized : DatetimeIndex

        Raises
        ------
        TypeError
            If the DatetimeIndex is tz-aware and tz is not None.
        """
        if self.tz is not None:
            if tz is None:
                new_dates = libts.tz_convert(self.asi8, 'UTC', self.tz)
            else:
                raise TypeError("Already tz-aware, use tz_convert to convert.")
        else:
            tz = timezones.maybe_get_tz(tz)
            # Convert to UTC

            new_dates = libts.tz_localize_to_utc(self.asi8, tz,
                                                 ambiguous=ambiguous,
                                                 errors=errors)
        new_dates = new_dates.view(_NS_DTYPE)
        return self._shallow_copy(new_dates, tz=tz)
