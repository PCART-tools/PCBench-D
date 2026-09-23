    def argsort(self, *args, **kwargs) -> npt.NDArray[np.intp]:
        """
        Returns the indices that would sort the index and its
        underlying data.

        Returns
        -------
        np.ndarray[np.intp]

        See Also
        --------
        numpy.ndarray.argsort
        """
        ascending = kwargs.pop("ascending", True)  # EA compat
        kwargs.pop("kind", None)  # e.g. "mergesort" is irrelevant
        nv.validate_argsort(args, kwargs)

        if self._range.step > 0:
            result = np.arange(len(self), dtype=np.intp)
        else:
            result = np.arange(len(self) - 1, -1, -1, dtype=np.intp)

        if not ascending:
            result = result[::-1]
        return result
