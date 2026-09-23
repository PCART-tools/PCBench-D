    def _convert_for_op(self, value):
        """ Convert value to be insertable to ndarray """
        if self._has_same_tz(value):
            return _to_M8(value)
        raise ValueError("Passed item and index have different timezone")
