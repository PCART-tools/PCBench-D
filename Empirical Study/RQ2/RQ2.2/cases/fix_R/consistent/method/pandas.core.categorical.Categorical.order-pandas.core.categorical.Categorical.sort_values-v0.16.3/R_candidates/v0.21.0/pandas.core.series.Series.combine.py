    def combine(self, other, func, fill_value=np.nan):
        """
        Perform elementwise binary operation on two Series using given function
        with optional fill value when an index is missing from one Series or
        the other

        Parameters
        ----------
        other : Series or scalar value
        func : function
        fill_value : scalar value

        Returns
        -------
        result : Series
        """
        if isinstance(other, Series):
            new_index = self.index.union(other.index)
            new_name = _maybe_match_name(self, other)
            new_values = np.empty(len(new_index), dtype=self.dtype)
            for i, idx in enumerate(new_index):
                lv = self.get(idx, fill_value)
                rv = other.get(idx, fill_value)
                with np.errstate(all='ignore'):
                    new_values[i] = func(lv, rv)
        else:
            new_index = self.index
            with np.errstate(all='ignore'):
                new_values = func(self._values, other)
            new_name = self.name
        return self._constructor(new_values, index=new_index, name=new_name)
