    def _addsub_offset_array(self, other, op):
        """
        Add or subtract array-like of DateOffset objects

        Parameters
        ----------
        other : Index, np.ndarray
            object-dtype containing pd.DateOffset objects
        op : {operator.add, operator.sub}

        Returns
        -------
        result : same class as self
        """
        assert op in [operator.add, operator.sub]
        if len(other) == 1:
            return op(self, other[0])

        warnings.warn("Adding/subtracting array of DateOffsets to "
                      "{cls} not vectorized"
                      .format(cls=type(self).__name__), PerformanceWarning)

        # For EA self.astype('O') returns a numpy array, not an Index
        left = lib.values_from_object(self.astype('O'))

        res_values = op(left, np.array(other))
        kwargs = {}
        if not is_period_dtype(self):
            kwargs['freq'] = 'infer'
        return self._from_sequence(res_values, **kwargs)
