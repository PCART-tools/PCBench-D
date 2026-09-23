    @classmethod
    def _generate(cls, start, end, periods, name, freq, closed=None):
        if com._count_not_none(start, end, periods, freq) != 3:
            raise ValueError('Of the four parameters: start, end, periods, '
                             'and freq, exactly three must be specified')

        if start is not None:
            start = Timedelta(start)

        if end is not None:
            end = Timedelta(end)

        left_closed = False
        right_closed = False

        if start is None and end is None:
            if closed is not None:
                raise ValueError("Closed has to be None if not both of start"
                                 "and end are defined")

        if closed is None:
            left_closed = True
            right_closed = True
        elif closed == "left":
            left_closed = True
        elif closed == "right":
            right_closed = True
        else:
            raise ValueError("Closed has to be either 'left', 'right' or None")

        if freq is not None:
            index = _generate_regular_range(start, end, periods, freq)
            index = cls._simple_new(index, name=name, freq=freq)
        else:
            index = to_timedelta(np.linspace(start.value, end.value, periods))

        if not left_closed:
            index = index[1:]
        if not right_closed:
            index = index[:-1]

        return index
