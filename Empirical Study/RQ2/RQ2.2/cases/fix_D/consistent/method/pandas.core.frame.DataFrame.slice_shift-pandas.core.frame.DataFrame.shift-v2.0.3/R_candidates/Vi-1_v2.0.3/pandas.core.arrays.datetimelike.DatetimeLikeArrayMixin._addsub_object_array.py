    @final
    def _addsub_object_array(self, other: npt.NDArray[np.object_], op):
        """
        Add or subtract array-like of DateOffset objects

        Parameters
        ----------
        other : np.ndarray[object]
        op : {operator.add, operator.sub}

        Returns
        -------
        np.ndarray[object]
            Except in fastpath case with length 1 where we operate on the
            contained scalar.
        """
        assert op in [operator.add, operator.sub]
        if len(other) == 1 and self.ndim == 1:
            # Note: without this special case, we could annotate return type
            #  as ndarray[object]
            # If both 1D then broadcasting is unambiguous
            return op(self, other[0])

        warnings.warn(
            "Adding/subtracting object-dtype array to "
            f"{type(self).__name__} not vectorized.",
            PerformanceWarning,
            stacklevel=find_stack_level(),
        )

        # Caller is responsible for broadcasting if necessary
        assert self.shape == other.shape, (self.shape, other.shape)

        res_values = op(self.astype("O"), np.asarray(other))
        return res_values
