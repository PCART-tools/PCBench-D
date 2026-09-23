    def get_values(self):
        """ same as values (but handles sparseness conversions); is a view """
        return self._data.values
