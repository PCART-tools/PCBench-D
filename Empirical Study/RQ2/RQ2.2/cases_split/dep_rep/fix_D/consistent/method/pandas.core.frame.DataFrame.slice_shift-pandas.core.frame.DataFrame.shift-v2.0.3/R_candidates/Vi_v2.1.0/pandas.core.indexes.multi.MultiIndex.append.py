    def append(self, other):
        """
        Append a collection of Index options together.

        Parameters
        ----------
        other : Index or list/tuple of indices

        Returns
        -------
        Index
            The combined index.

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([['a'], ['b']])
        >>> mi
        MultiIndex([('a', 'b')],
                   )
        >>> mi.append(mi)
        MultiIndex([('a', 'b'), ('a', 'b')],
                   )
        """
        if not isinstance(other, (list, tuple)):
            other = [other]

        if all(
            (isinstance(o, MultiIndex) and o.nlevels >= self.nlevels) for o in other
        ):
            codes = []
            levels = []
            names = []
            for i in range(self.nlevels):
                level_values = self.levels[i]
                for mi in other:
                    level_values = level_values.union(mi.levels[i])
                level_codes = [
                    recode_for_categories(
                        mi.codes[i], mi.levels[i], level_values, copy=False
                    )
                    for mi in ([self, *other])
                ]
                level_name = self.names[i]
                if any(mi.names[i] != level_name for mi in other):
                    level_name = None
                codes.append(np.concatenate(level_codes))
                levels.append(level_values)
                names.append(level_name)
            return MultiIndex(
                codes=codes, levels=levels, names=names, verify_integrity=False
            )

        to_concat = (self._values,) + tuple(k._values for k in other)
        new_tuples = np.concatenate(to_concat)

        # if all(isinstance(x, MultiIndex) for x in other):
        try:
            # We only get here if other contains at least one index with tuples,
            # setting names to None automatically
            return MultiIndex.from_tuples(new_tuples)
        except (TypeError, IndexError):
            return Index(new_tuples)
