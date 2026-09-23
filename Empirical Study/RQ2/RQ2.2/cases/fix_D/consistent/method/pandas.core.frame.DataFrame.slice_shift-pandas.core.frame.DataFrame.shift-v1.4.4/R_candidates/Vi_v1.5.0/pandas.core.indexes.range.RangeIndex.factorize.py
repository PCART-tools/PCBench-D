    def factorize(
        self,
        sort: bool = False,
        na_sentinel: int | lib.NoDefault = lib.no_default,
        use_na_sentinel: bool | lib.NoDefault = lib.no_default,
    ) -> tuple[npt.NDArray[np.intp], RangeIndex]:
        # resolve to emit warning if appropriate
        resolve_na_sentinel(na_sentinel, use_na_sentinel)
        codes = np.arange(len(self), dtype=np.intp)
        uniques = self
        if sort and self.step < 0:
            codes = codes[::-1]
            uniques = uniques[::-1]
        return codes, uniques
