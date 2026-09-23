    def _validate_fill_value(self, value):
        """
        Convert value to be insertable to ndarray.
        """
        return self._data._validate_setitem_value(value)
