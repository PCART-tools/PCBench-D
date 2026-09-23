    def _is_level_reference(self, key, axis=0):
        """
        Test whether a key is a level reference for a given axis.

        To be considered a level reference, `key` must be a string that:
          - (axis=0): Matches the name of an index level and does NOT match
            a column label.
          - (axis=1): Matches the name of a column level and does NOT match
            an index label.

        Parameters
        ----------
        key : str
            Potential level name for the given axis
        axis : int, default 0
            Axis that levels are associated with (0 for index, 1 for columns)

        Returns
        -------
        is_level : bool
        """
        axis = self._get_axis_number(axis)

        if self.ndim > 2:
            raise NotImplementedError(
                "_is_level_reference is not implemented for {type}"
                .format(type=type(self)))

        return (key is not None and
                is_hashable(key) and
                key in self.axes[axis].names and
                not self._is_label_reference(key, axis=axis))
