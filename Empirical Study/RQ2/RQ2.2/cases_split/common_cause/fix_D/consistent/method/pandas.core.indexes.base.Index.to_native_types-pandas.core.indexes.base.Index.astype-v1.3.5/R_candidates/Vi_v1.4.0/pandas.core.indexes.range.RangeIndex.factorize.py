    def factorize(
        self, sort: bool = False, na_sentinel: int | None = -1
    ) -> tuple[npt.NDArray[np.intp], RangeIndex]:
        codes = np.arange(len(self), dtype=np.intp)
        uniques = self
        if sort and self.step < 0:
            codes = codes[::-1]
            uniques = uniques[::-1]
        return codes, uniques
