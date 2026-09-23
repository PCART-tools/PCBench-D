    def indexer_between_time(self, start_time, end_time, include_start=True,
                             include_end=True):
        """
        Return index locations of values between particular times of day
        (e.g., 9:00-9:30AM).

        Parameters
        ----------
        start_time, end_time : datetime.time, str
            datetime.time or string in appropriate format ("%H:%M", "%H%M",
            "%I:%M%p", "%I%M%p", "%H:%M:%S", "%H%M%S", "%I:%M:%S%p",
            "%I%M%S%p").
        include_start : boolean, default True
        include_end : boolean, default True

        Returns
        -------
        values_between_time : array of integers

        See Also
        --------
        indexer_at_time, DataFrame.between_time
        """
        start_time = tools.to_time(start_time)
        end_time = tools.to_time(end_time)
        time_micros = self._get_time_micros()
        start_micros = _time_to_micros(start_time)
        end_micros = _time_to_micros(end_time)

        if include_start and include_end:
            lop = rop = operator.le
        elif include_start:
            lop = operator.le
            rop = operator.lt
        elif include_end:
            lop = operator.lt
            rop = operator.le
        else:
            lop = rop = operator.lt

        if start_time <= end_time:
            join_op = operator.and_
        else:
            join_op = operator.or_

        mask = join_op(lop(start_micros, time_micros),
                       rop(time_micros, end_micros))

        return mask.nonzero()[0]
