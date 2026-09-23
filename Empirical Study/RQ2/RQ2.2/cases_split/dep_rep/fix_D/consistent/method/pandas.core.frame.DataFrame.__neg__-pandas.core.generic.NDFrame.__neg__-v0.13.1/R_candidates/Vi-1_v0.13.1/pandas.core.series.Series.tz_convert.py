    def tz_convert(self, tz, copy=True):
        """
        Convert TimeSeries to target time zone

        Parameters
        ----------
        tz : string or pytz.timezone object
        copy : boolean, default True
            Also make a copy of the underlying data

        Returns
        -------
        converted : TimeSeries
        """
        new_index = self.index.tz_convert(tz)

        new_values = self.values
        if copy:
            new_values = new_values.copy()

        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
