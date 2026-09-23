    @property
    def is_monotonic_decreasing(self):
        """
        Return boolean if values in the object are
        monotonic_decreasing

        .. versionadded:: 0.19.0

        Returns
        -------
        is_monotonic_decreasing : boolean
        """
        from pandas import Index
        return Index(self).is_monotonic_decreasing
