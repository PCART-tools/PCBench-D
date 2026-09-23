    def argmax(self, skipna: bool = True) -> int:
        """
        Return the index of maximum value.

        In case of multiple occurrences of the maximum value, the index
        corresponding to the first occurrence is returned.

        Parameters
        ----------
        skipna : bool, default True

        Returns
        -------
        int

        See Also
        --------
        ExtensionArray.argmin
        """
        # Implementor note: You have two places to override the behavior of
        # argmax.
        # 1. _values_for_argsort : construct the values used in nargminmax
        # 2. argmax itself : total control over sorting.
        validate_bool_kwarg(skipna, "skipna")
        if not skipna and self._hasna:
            raise NotImplementedError
        return nargminmax(self, "argmax")
