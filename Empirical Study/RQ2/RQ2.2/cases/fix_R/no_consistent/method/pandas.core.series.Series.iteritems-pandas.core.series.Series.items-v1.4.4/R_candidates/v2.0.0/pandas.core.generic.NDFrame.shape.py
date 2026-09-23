    @property
    def shape(self) -> tuple[int, ...]:
        """
        Return a tuple of axis dimensions
        """
        return tuple(len(self._get_axis(a)) for a in self._AXIS_ORDERS)
