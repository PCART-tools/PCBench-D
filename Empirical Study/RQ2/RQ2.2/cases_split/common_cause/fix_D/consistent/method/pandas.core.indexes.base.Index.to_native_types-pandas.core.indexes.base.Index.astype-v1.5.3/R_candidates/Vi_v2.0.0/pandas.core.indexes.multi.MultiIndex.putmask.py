    def putmask(self, mask, value: MultiIndex) -> MultiIndex:
        """
        Return a new MultiIndex of the values set with the mask.

        Parameters
        ----------
        mask : array like
        value : MultiIndex
            Must either be the same length as self or length one

        Returns
        -------
        MultiIndex
        """
        mask, noop = validate_putmask(self, mask)
        if noop:
            return self.copy()

        if len(mask) == len(value):
            subset = value[mask].remove_unused_levels()
        else:
            subset = value.remove_unused_levels()

        new_levels = []
        new_codes = []

        for i, (value_level, level, level_codes) in enumerate(
            zip(subset.levels, self.levels, self.codes)
        ):
            new_level = level.union(value_level, sort=False)
            value_codes = new_level.get_indexer_for(subset.get_level_values(i))
            new_code = ensure_int64(level_codes)
            new_code[mask] = value_codes
            new_levels.append(new_level)
            new_codes.append(new_code)

        return MultiIndex(
            levels=new_levels, codes=new_codes, names=self.names, verify_integrity=False
        )
