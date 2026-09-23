    @final
    def _drop_labels_or_levels(self, keys, axis: AxisInt = 0):
        """
        Drop labels and/or levels for the given `axis`.

        For each key in `keys`:
          - (axis=0): If key matches a column label then drop the column.
            Otherwise if key matches an index level then drop the level.
          - (axis=1): If key matches an index label then drop the row.
            Otherwise if key matches a column level then drop the level.

        Parameters
        ----------
        keys : str or list of str
            labels or levels to drop
        axis : int, default 0
            Axis that levels are associated with (0 for index, 1 for columns)

        Returns
        -------
        dropped: DataFrame

        Raises
        ------
        ValueError
            if any `keys` match neither a label nor a level
        """
        axis = self._get_axis_number(axis)

        # Validate keys
        keys = common.maybe_make_list(keys)
        invalid_keys = [
            k for k in keys if not self._is_label_or_level_reference(k, axis=axis)
        ]

        if invalid_keys:
            raise ValueError(
                "The following keys are not valid labels or "
                f"levels for axis {axis}: {invalid_keys}"
            )

        # Compute levels and labels to drop
        levels_to_drop = [k for k in keys if self._is_level_reference(k, axis=axis)]

        labels_to_drop = [k for k in keys if not self._is_level_reference(k, axis=axis)]

        # Perform copy upfront and then use inplace operations below.
        # This ensures that we always perform exactly one copy.
        # ``copy`` and/or ``inplace`` options could be added in the future.
        dropped = self.copy(deep=False)

        if axis == 0:
            # Handle dropping index levels
            if levels_to_drop:
                dropped.reset_index(levels_to_drop, drop=True, inplace=True)

            # Handle dropping columns labels
            if labels_to_drop:
                dropped.drop(labels_to_drop, axis=1, inplace=True)
        else:
            # Handle dropping column levels
            if levels_to_drop:
                if isinstance(dropped.columns, MultiIndex):
                    # Drop the specified levels from the MultiIndex
                    dropped.columns = dropped.columns.droplevel(levels_to_drop)
                else:
                    # Drop the last level of Index by replacing with
                    # a RangeIndex
                    dropped.columns = RangeIndex(dropped.columns.size)

            # Handle dropping index labels
            if labels_to_drop:
                dropped.drop(labels_to_drop, axis=0, inplace=True)

        return dropped
