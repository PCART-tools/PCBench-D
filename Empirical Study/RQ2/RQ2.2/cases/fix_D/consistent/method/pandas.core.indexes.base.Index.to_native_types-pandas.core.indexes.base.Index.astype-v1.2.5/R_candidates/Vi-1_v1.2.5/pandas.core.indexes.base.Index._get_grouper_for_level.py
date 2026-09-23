    def _get_grouper_for_level(self, mapper, level=None):
        """
        Get index grouper corresponding to an index level

        Parameters
        ----------
        mapper: Group mapping function or None
            Function mapping index values to groups
        level : int or None
            Index level

        Returns
        -------
        grouper : Index
            Index of values to group on.
        labels : ndarray of int or None
            Array of locations in level_index.
        uniques : Index or None
            Index of unique values for level.
        """
        assert level is None or level == 0
        if mapper is None:
            grouper = self
        else:
            grouper = self.map(mapper)

        return grouper, None, None
