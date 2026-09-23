    def _formatting_values(self):
        """
        Return the values that can be formatted (used by SeriesFormatter
        and DataFrameFormatter).
        """
        return self._data.formatting_values()
