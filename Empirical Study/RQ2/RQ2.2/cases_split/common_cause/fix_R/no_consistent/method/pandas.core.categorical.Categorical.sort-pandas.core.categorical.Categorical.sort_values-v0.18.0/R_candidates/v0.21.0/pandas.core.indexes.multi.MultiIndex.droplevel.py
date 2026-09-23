    def droplevel(self, level=0):
        """
        Return Index with requested level removed. If MultiIndex has only 2
        levels, the result will be of Index type not MultiIndex.

        Parameters
        ----------
        level : int/level name or list thereof

        Notes
        -----
        Does not check if result index is unique or not

        Returns
        -------
        index : Index or MultiIndex
        """
        levels = level
        if not isinstance(levels, (tuple, list)):
            levels = [level]

        new_levels = list(self.levels)
        new_labels = list(self.labels)
        new_names = list(self.names)

        levnums = sorted(self._get_level_number(lev) for lev in levels)[::-1]

        for i in levnums:
            new_levels.pop(i)
            new_labels.pop(i)
            new_names.pop(i)

        if len(new_levels) == 1:

            # set nan if needed
            mask = new_labels[0] == -1
            result = new_levels[0].take(new_labels[0])
            if mask.any():
                result = result.putmask(mask, np.nan)

            result.name = new_names[0]
            return result
        else:
            return MultiIndex(levels=new_levels, labels=new_labels,
                              names=new_names, verify_integrity=False)
