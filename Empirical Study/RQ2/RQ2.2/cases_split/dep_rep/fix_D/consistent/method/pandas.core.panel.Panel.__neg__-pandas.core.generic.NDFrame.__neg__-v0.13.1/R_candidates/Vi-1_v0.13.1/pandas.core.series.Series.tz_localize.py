    def tz_localize(self, tz, copy=True, infer_dst=False):
        """
        Localize tz-naive TimeSeries to target time zone
        Entries will retain their "naive" value but will be annotated as
        being relative to the specified tz.

        After localizing the TimeSeries, you may use tz_convert() to
        get the Datetime values recomputed to a different tz.

        Parameters
        ----------
        tz : string or pytz.timezone object
        copy : boolean, default True
            Also make a copy of the underlying data
        infer_dst : boolean, default False
            Attempt to infer fall dst-transition hours based on order

        Returns
        -------
        localized : TimeSeries
        """
        from pandas.tseries.index import DatetimeIndex

        if not isinstance(self.index, DatetimeIndex):
            if len(self.index) > 0:
                raise Exception('Cannot tz-localize non-time series')

            new_index = DatetimeIndex([], tz=tz)
        else:
            new_index = self.index.tz_localize(tz, infer_dst=infer_dst)

        new_values = self.values
        if copy:
            new_values = new_values.copy()

        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
