    def __iter__(self):
        """
        Resampler iterator.

        Returns
        -------
        Generator yielding sequence of (name, subsetted object)
        for each group.

        See Also
        --------
        GroupBy.__iter__
        """
        self._set_binner()
        return super().__iter__()
