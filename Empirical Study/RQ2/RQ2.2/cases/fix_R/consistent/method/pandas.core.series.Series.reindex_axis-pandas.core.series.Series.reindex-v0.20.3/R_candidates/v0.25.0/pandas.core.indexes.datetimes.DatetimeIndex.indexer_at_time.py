    def indexer_at_time(self, time, asof=False):
        """
        Return index locations of index values at particular time of day
        (e.g. 9:30AM).

        Parameters
        ----------
        time : datetime.time or string
            datetime.time or string in appropriate format ("%H:%M", "%H%M",
            "%I:%M%p", "%I%M%p", "%H:%M:%S", "%H%M%S", "%I:%M:%S%p",
            "%I%M%S%p").

        Returns
        -------
        values_at_time : array of integers

        See Also
        --------
        indexer_between_time, DataFrame.at_time
        """
        if asof:
            raise NotImplementedError("'asof' argument is not supported")

        if isinstance(time, str):
            from dateutil.parser import parse

            time = parse(time).time()

        if time.tzinfo:
            if self.tz is None:
                raise ValueError("Index must be timezone aware.")
            time_micros = self.tz_convert(time.tzinfo)._get_time_micros()
        else:
            time_micros = self._get_time_micros()
        micros = _time_to_micros(time)
        return (micros == time_micros).nonzero()[0]
