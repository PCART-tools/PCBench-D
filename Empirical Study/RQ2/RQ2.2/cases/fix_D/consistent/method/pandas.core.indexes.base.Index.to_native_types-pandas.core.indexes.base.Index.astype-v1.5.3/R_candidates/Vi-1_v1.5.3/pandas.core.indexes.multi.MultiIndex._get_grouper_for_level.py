    @doc(Index._get_grouper_for_level)
    def _get_grouper_for_level(
        self,
        mapper,
        *,
        level=None,
        dropna: bool = True,
    ) -> tuple[Index, npt.NDArray[np.signedinteger] | None, Index | None]:
        if mapper is not None:
            indexer = self.codes[level]
            # Handle group mapping function and return
            level_values = self.levels[level].take(indexer)
            grouper = level_values.map(mapper)
            return grouper, None, None

        values = self.get_level_values(level)
        codes, uniques = algos.factorize(values, sort=True, use_na_sentinel=dropna)
        assert isinstance(uniques, Index)

        if self.levels[level]._can_hold_na:
            grouper = uniques.take(codes, fill_value=True)
        else:
            grouper = uniques.take(codes)

        return grouper, codes, uniques
