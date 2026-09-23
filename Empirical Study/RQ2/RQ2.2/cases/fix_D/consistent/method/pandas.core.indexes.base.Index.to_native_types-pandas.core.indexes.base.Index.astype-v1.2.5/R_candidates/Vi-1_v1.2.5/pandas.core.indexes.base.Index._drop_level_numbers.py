    def _drop_level_numbers(self, levnums: List[int]):
        """
        Drop MultiIndex levels by level _number_, not name.
        """

        if len(levnums) == 0:
            return self
        if len(levnums) >= self.nlevels:
            raise ValueError(
                f"Cannot remove {len(levnums)} levels from an index with "
                f"{self.nlevels} levels: at least one level must be left."
            )
        # The two checks above guarantee that here self is a MultiIndex
        self = cast("MultiIndex", self)

        new_levels = list(self.levels)
        new_codes = list(self.codes)
        new_names = list(self.names)

        for i in levnums:
            new_levels.pop(i)
            new_codes.pop(i)
            new_names.pop(i)

        if len(new_levels) == 1:

            # set nan if needed
            mask = new_codes[0] == -1
            result = new_levels[0].take(new_codes[0])
            if mask.any():
                result = result.putmask(mask, np.nan)

            result._name = new_names[0]
            return result
        else:
            from pandas.core.indexes.multi import MultiIndex

            return MultiIndex(
                levels=new_levels,
                codes=new_codes,
                names=new_names,
                verify_integrity=False,
            )
