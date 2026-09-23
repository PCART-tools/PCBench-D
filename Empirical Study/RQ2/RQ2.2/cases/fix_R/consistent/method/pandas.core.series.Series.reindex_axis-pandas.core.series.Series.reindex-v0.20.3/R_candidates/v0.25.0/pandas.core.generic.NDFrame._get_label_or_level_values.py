    def _get_label_or_level_values(self, key, axis=0):
        """
        Return a 1-D array of values associated with `key`, a label or level
        from the given `axis`.

        Retrieval logic:
          - (axis=0): Return column values if `key` matches a column label.
            Otherwise return index level values if `key` matches an index
            level.
          - (axis=1): Return row values if `key` matches an index label.
            Otherwise return column level values if 'key' matches a column
            level

        Parameters
        ----------
        key: str
            Label or level name.
        axis: int, default 0
            Axis that levels are associated with (0 for index, 1 for columns)

        Returns
        -------
        values: np.ndarray

        Raises
        ------
        KeyError
            if `key` matches neither a label nor a level
        ValueError
            if `key` matches multiple labels
        FutureWarning
            if `key` is ambiguous. This will become an ambiguity error in a
            future version
        """
        axis = self._get_axis_number(axis)
        other_axes = [ax for ax in range(self._AXIS_LEN) if ax != axis]

        if self._is_label_reference(key, axis=axis):
            self._check_label_or_level_ambiguity(key, axis=axis)
            values = self.xs(key, axis=other_axes[0])._values
        elif self._is_level_reference(key, axis=axis):
            values = self.axes[axis].get_level_values(key)._values
        else:
            raise KeyError(key)

        # Check for duplicates
        if values.ndim > 1:

            if other_axes and isinstance(self._get_axis(other_axes[0]), MultiIndex):
                multi_message = (
                    "\n"
                    "For a multi-index, the label must be a "
                    "tuple with elements corresponding to "
                    "each level."
                )
            else:
                multi_message = ""

            label_axis_name = "column" if axis == 0 else "index"
            raise ValueError(
                (
                    "The {label_axis_name} label '{key}' "
                    "is not unique.{multi_message}"
                ).format(
                    key=key,
                    label_axis_name=label_axis_name,
                    multi_message=multi_message,
                )
            )

        return values
