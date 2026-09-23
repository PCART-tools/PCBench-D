    def _deepcopy_if_needed(self, orig, copy=False):
        """
        .. versionadded:: 0.19.0

        Make a copy of self if data coincides (in memory) with orig.
        Subclasses should override this if self._base is not an ndarray.

        Parameters
        ----------
        orig : ndarray
            other ndarray to compare self._data against
        copy : boolean, default False
            when False, do not run any check, just return self

        Returns
        -------
        A copy of self if needed, otherwise self : Index
        """
        if copy:
            # Retrieve the "base objects", i.e. the original memory allocations
            if not isinstance(orig, np.ndarray):
                # orig is a DatetimeIndex
                orig = orig.values
            orig = orig if orig.base is None else orig.base
            new = self._data if self._data.base is None else self._data.base
            if orig is new:
                return self.copy(deep=True)

        return self
