    def copy(self, deep=True):
        """
        Make a copy of this SparseDataFrame
        """
        result = super().copy(deep=deep)
        result._default_fill_value = self._default_fill_value
        result._default_kind = self._default_kind
        return result
