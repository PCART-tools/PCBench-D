    def _check_label_or_level_ambiguity(self, key, axis=0):
        """
        Check whether `key` is ambiguous.

        By ambiguous, we mean that it matches both a level of the input
        `axis` and a label of the other axis.

        Parameters
        ----------
        key: str or object
            label or level name
        axis: int, default 0
            Axis that levels are associated with (0 for index, 1 for columns)

        Raises
        ------
        ValueError: `key` is ambiguous
        """

        axis = self._get_axis_number(axis)
        other_axes = [ax for ax in range(self._AXIS_LEN) if ax != axis]

        if self.ndim > 2:
            raise NotImplementedError(
                "_check_label_or_level_ambiguity is not implemented for {type}"
                .format(type=type(self)))

        if (key is not None and
                is_hashable(key) and
                key in self.axes[axis].names and
                any(key in self.axes[ax] for ax in other_axes)):

            # Build an informative and grammatical warning
            level_article, level_type = (('an', 'index')
                                         if axis == 0 else
                                         ('a', 'column'))

            label_article, label_type = (('a', 'column')
                                         if axis == 0 else
                                         ('an', 'index'))

            msg = ("'{key}' is both {level_article} {level_type} level and "
                   "{label_article} {label_type} label, which is ambiguous."
                   ).format(key=key,
                            level_article=level_article,
                            level_type=level_type,
                            label_article=label_article,
                            label_type=label_type)
            raise ValueError(msg)
