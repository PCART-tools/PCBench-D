    @classmethod
    def concat_horizontal(cls, mgrs: list[Self], axes: list[Index]) -> Self:
        """
        Concatenate uniformly-indexed ArrayManagers horizontally.
        """
        # concatting along the columns -> combine reindexed arrays in a single manager
        arrays = list(itertools.chain.from_iterable([mgr.arrays for mgr in mgrs]))
        new_mgr = cls(arrays, [axes[1], axes[0]], verify_integrity=False)
        return new_mgr
