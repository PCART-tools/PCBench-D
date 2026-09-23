    def _check_label_or_level_ambiguity(self, key, axis=0, stacklevel=1):
        """
        Check whether `key` matches both a level of the input `axis` and a
        label of the other axis and raise a ``FutureWarning`` if this is the
        case.

        Note: This method will be altered to raise an ambiguity exception in
        a future version.

        Parameters
        ----------
        key: str or object
            label or level name
        axis: int, default 0
            Axis that levels are associated with (0 for index, 1 for columns)
        stacklevel: int, default 1
            Stack level used when a FutureWarning is raised (see below).

        Returns
        -------
        ambiguous: bool

        Raises
        ------
        FutureWarning
            if `key` is ambiguous. This will become an ambiguity error in a
            future version
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
                   "{label_article} {label_type} label.\n"
                   "Defaulting to {label_type}, but this will raise an "
                   "ambiguity error in a future version"
                   ).format(key=key,
                            level_article=level_article,
                            level_type=level_type,
                            label_article=label_article,
                            label_type=label_type)

            warnings.warn(msg, FutureWarning, stacklevel=stacklevel + 1)
            return True
        else:
            return False
