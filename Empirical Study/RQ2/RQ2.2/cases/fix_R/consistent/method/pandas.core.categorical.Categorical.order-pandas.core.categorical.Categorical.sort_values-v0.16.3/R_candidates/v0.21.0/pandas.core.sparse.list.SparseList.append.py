    def append(self, value):
        """
        Append element or array-like chunk of data to the SparseList

        Parameters
        ----------
        value: scalar or array-like
        """
        if is_scalar(value):
            value = [value]

        sparr = SparseArray(value, fill_value=self.fill_value)
        self._chunks.append(sparr)
        self._consolidated = False
