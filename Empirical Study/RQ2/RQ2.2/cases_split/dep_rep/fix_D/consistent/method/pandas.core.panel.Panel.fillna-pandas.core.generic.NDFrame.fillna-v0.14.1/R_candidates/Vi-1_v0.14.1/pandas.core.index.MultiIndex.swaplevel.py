    def swaplevel(self, i, j):
        """
        Swap level i with level j. Do not change the ordering of anything

        Parameters
        ----------
        i, j : int, string (can be mixed)
            Level of index to be swapped. Can pass level name as string.

        Returns
        -------
        swapped : MultiIndex
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
