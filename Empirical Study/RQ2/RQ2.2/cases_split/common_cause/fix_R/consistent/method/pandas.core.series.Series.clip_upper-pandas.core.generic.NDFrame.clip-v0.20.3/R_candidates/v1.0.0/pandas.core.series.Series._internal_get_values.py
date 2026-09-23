    def _internal_get_values(self):
        """
        Same as values (but handles sparseness conversions); is a view.

        Returns
        -------
        numpy.ndarray
            Data of the Series.
        """

        return self._data.get_values()
