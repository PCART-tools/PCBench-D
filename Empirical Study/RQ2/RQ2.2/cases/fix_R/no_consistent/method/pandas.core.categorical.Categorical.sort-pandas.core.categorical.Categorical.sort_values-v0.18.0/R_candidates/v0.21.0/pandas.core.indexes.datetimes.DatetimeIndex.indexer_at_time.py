    def indexer_at_time(self, time, asof=False):
        """
        Select values at particular time of day (e.g. 9:30AM)

        Parameters
        ----------
        time : datetime.time or string

        Returns
        -------
        values_at_time : TimeSeries
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
