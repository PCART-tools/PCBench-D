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
        if len(other) == 1 and self.ndim == 1:
            # If both 1D then broadcasting is unambiguous
            return op(self, other[0])

        warnings.warn(
            "Adding/subtracting object-dtype array to "
            f"{type(self).__name__} not vectorized.",
            PerformanceWarning,
        )

        # Caller is responsible for broadcasting if necessary
        assert self.shape == other.shape, (self.shape, other.shape)

        with warnings.catch_warnings():
            # filter out warnings about Timestamp.freq
            warnings.filterwarnings("ignore", category=FutureWarning)
            res_values = op(self.astype("O"), np.asarray(other))

        result = pd_array(res_values.ravel())
        # error: Item "ExtensionArray" of "Union[Any, ExtensionArray]" has no attribute
        # "reshape"
        result = extract_array(
            result, extract_numpy=True
        ).reshape(  # type: ignore[union-attr]
            self.shape
        )
        return result
