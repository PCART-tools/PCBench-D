    def indexer_at_time(self, time, asof=False):
        """
        Returns index locations of index values at particular time of day
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
        from dateutil.parser import parse

        if asof:
            raise NotImplementedError("'asof' argument is not supported")

        if isinstance(time, compat.string_types):
            time = parse(time).time()

        if time.tzinfo:
            # TODO
            raise NotImplementedError("argument 'time' with timezone info is "
                                      "not supported")

        time_micros = self._get_time_micros()
        micros = _time_to_micros(time)
        return (micros == time_micros).nonzero()[0]
