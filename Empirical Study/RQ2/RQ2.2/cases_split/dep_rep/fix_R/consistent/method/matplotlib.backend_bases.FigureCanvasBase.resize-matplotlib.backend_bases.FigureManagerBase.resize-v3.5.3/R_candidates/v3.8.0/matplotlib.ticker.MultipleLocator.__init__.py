    def __init__(self, base=1.0, offset=0.0):
        """
        Parameters
        ----------
        base : float > 0
            Interval between ticks.
        offset : float
            Value added to each multiple of *base*.

            .. versionadded:: 3.8
        """
        self._edge = _Edge_integer(base, 0)
        self._offset = offset
