    def __iter__(self) -> Iterator:
        """
        Iterate over info axis.

        Returns
        -------
        iterator
            Info axis as iterator.
        """
        return iter(self._info_axis)
