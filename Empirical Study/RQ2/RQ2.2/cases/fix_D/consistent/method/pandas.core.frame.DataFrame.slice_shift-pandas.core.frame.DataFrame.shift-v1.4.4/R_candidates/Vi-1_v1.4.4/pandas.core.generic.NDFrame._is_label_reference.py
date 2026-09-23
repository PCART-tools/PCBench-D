    @final
    def _is_label_reference(self, key, axis=0) -> bool_t:
        """
        Test whether a key is a label reference for a given axis.

        To be considered a label reference, `key` must be a string that:
          - (axis=0): Matches a column label
          - (axis=1): Matches an index label

        Parameters
        ----------
        key : str
            Potential label name
        axis : int, default 0
            Axis perpendicular to the axis that labels are associated with
            (0 means search for column labels, 1 means search for index labels)

        Returns
        -------
        is_label: bool
        """
        axis = self._get_axis_number(axis)
        other_axes = (ax for ax in range(self._AXIS_LEN) if ax != axis)

        return (
            key is not None
            and is_hashable(key)
            and any(key in self.axes[ax] for ax in other_axes)
        )
