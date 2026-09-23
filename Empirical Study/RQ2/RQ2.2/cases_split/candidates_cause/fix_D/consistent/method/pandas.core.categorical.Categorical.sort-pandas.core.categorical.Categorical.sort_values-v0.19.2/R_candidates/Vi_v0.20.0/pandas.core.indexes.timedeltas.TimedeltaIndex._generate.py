    @classmethod
    def _generate(cls, start, end, periods, name, offset, closed=None):
        if com._count_not_none(start, end, periods) != 2:
            raise ValueError('Must specify two of start, end, or periods')

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

        index = _generate_regular_range(start, end, periods, offset)
        index = cls._simple_new(index, name=name, freq=offset)

        if not left_closed:
            index = index[1:]
        if not right_closed:
            index = index[:-1]

        return index
