    @final
    def _check_label_or_level_ambiguity(self, key: Level, axis: Axis = 0) -> None:
        """
        Check whether `key` is ambiguous.

        By ambiguous, we mean that it matches both a level of the input
        `axis` and a label of the other axis.

        Parameters
        ----------
        key : Hashable
            Label or level name.
        axis : int, default 0
            Axis that levels are associated with (0 for index, 1 for columns).

        Raises
        ------
        ValueError: `key` is ambiguous
        """

        axis_int = self._get_axis_number(axis)
        other_axes = (ax for ax in range(self._AXIS_LEN) if ax != axis_int)

        if (
            key is not None
            and is_hashable(key)
            and key in self.axes[axis_int].names
            and any(key in self.axes[ax] for ax in other_axes)
        ):
            # Build an informative and grammatical warning
            level_article, level_type = (
                ("an", "index") if axis_int == 0 else ("a", "column")
            )

            label_article, label_type = (
                ("a", "column") if axis_int == 0 else ("an", "index")
            )

            msg = (
                f"'{key}' is both {level_article} {level_type} level and "
                f"{label_article} {label_type} label, which is ambiguous."
            )
            raise ValueError(msg)
