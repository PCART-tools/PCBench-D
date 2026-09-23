    @staticmethod
    def convert(value, unit, axis):
        """
        If *value* is not already a number or sequence of numbers,
        convert it with :func:`date2num`.

        The *unit* and *axis* arguments are not used.
        """
        if units.ConversionInterface.is_numlike(value):
            return value
        return date2num(value)
