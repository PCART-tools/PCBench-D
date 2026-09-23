    def _addsub_object_array(self, other: np.ndarray, op):
        """
        Add or subtract array-like of DateOffset objects

        Parameters
        ----------
        other : np.ndarray[object]
        op : {operator.add, operator.sub}

        Returns
        -------
        result : same class as self
        """
        assert op in [operator.add, operator.sub]
        if len(other) == 1:
            return op(self, other[0])

        warnings.warn(
            "Adding/subtracting array of DateOffsets to "
            f"{type(self).__name__} not vectorized",
            PerformanceWarning,
        )

        # For EA self.astype('O') returns a numpy array, not an Index
        left = self.astype("O")

        res_values = op(left, np.array(other))
        kwargs = {}
        if not is_period_dtype(self):
            kwargs["freq"] = "infer"
        try:
            res = type(self)._from_sequence(res_values, **kwargs)
        except ValueError:
            # e.g. we've passed a Timestamp to TimedeltaArray
            res = res_values
        return res
