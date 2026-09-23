    @final
    def _is_label_or_level_reference(self, key: Level, axis: AxisInt = 0) -> bool_t:
        """
        Test whether a key is a label or level reference for a given axis.

        To be considered either a label or a level reference, `key` must be a
        string that:
          - (axis=0): Matches a column label or an index level
          - (axis=1): Matches an index label or a column level

        Parameters
        ----------
        key : Hashable
            Potential label or level name
        axis : int, default 0
            Axis that levels are associated with (0 for index, 1 for columns)

        Returns
        -------
        bool
        """
        return self._is_level_reference(key, axis=axis) or self._is_label_reference(
            key, axis=axis
        )
