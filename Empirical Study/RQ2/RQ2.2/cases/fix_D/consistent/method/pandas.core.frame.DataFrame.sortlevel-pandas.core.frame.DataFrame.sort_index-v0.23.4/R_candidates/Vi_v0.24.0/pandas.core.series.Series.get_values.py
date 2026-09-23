    def get_values(self):
        """
        Same as values (but handles sparseness conversions); is a view.
        """
        return self._data.get_values()
