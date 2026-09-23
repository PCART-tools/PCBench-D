    @property
    def is_monotonic(self):
        """
        Return boolean if values in the object are
        monotonic_increasing

        .. versionadded:: 0.19.0

        Returns
        -------
        is_monotonic : boolean
        """
        from pandas import Index
        return Index(self).is_monotonic
