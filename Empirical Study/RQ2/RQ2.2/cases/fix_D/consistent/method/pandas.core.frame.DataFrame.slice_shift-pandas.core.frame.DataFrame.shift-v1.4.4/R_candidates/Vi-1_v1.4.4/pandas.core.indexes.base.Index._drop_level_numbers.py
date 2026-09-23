    @final
    def _drop_level_numbers(self, levnums: list[int]):
        """
        Drop MultiIndex levels by level _number_, not name.
        """

        if not levnums and not isinstance(self, ABCMultiIndex):
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
            lev = new_levels[0]

            if len(lev) == 0:
                # If lev is empty, lev.take will fail GH#42055
                if len(new_codes[0]) == 0:
                    # GH#45230 preserve RangeIndex here
                    #  see test_reset_index_empty_rangeindex
                    result = lev[:0]
                else:
                    res_values = algos.take(lev._values, new_codes[0], allow_fill=True)
                    # _constructor instead of type(lev) for RangeIndex compat GH#35230
                    result = lev._constructor._simple_new(res_values, name=new_names[0])
            else:
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
