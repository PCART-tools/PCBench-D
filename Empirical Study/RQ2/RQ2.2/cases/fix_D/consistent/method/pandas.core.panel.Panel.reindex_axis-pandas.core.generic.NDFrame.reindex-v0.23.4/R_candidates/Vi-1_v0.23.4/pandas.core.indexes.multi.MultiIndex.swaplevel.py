    def swaplevel(self, i=-2, j=-1):
        """
        Swap level i with level j.

        Calling this method does not change the ordering of the values.

        Parameters
        ----------
        i : int, str, default -2
            First level of index to be swapped. Can pass level name as string.
            Type of parameters can be mixed.
        j : int, str, default -1
            Second level of index to be swapped. Can pass level name as string.
            Type of parameters can be mixed.

        Returns
        -------
        MultiIndex
            A new MultiIndex

        .. versionchanged:: 0.18.1

           The indexes ``i`` and ``j`` are now optional, and default to
           the two innermost levels of the index.

        See Also
        --------
        Series.swaplevel : Swap levels i and j in a MultiIndex
        Dataframe.swaplevel : Swap levels i and j in a MultiIndex on a
            particular axis

        Examples
        --------
        >>> mi = pd.MultiIndex(levels=[['a', 'b'], ['bb', 'aa']],
        ...                    labels=[[0, 0, 1, 1], [0, 1, 0, 1]])
        >>> mi
        MultiIndex(levels=[['a', 'b'], ['bb', 'aa']],
           labels=[[0, 0, 1, 1], [0, 1, 0, 1]])
        >>> mi.swaplevel(0, 1)
        MultiIndex(levels=[['bb', 'aa'], ['a', 'b']],
           labels=[[0, 1, 0, 1], [0, 0, 1, 1]])
        """
        new_levels = list(self.levels)
        new_labels = list(self.labels)
        new_names = list(self.names)

        i = self._get_level_number(i)
        j = self._get_level_number(j)

        new_levels[i], new_levels[j] = new_levels[j], new_levels[i]
        new_labels[i], new_labels[j] = new_labels[j], new_labels[i]
        new_names[i], new_names[j] = new_names[j], new_names[i]

        return MultiIndex(levels=new_levels, labels=new_labels,
                          names=new_names, verify_integrity=False)
