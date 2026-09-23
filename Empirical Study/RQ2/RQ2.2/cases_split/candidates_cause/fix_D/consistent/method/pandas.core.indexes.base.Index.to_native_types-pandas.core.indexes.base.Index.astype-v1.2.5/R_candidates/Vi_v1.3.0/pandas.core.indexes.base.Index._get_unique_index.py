    def _get_unique_index(self: _IndexT) -> _IndexT:
        """
        Returns an index containing unique values.

        Returns
        -------
        Index
        """
        return self.unique()
