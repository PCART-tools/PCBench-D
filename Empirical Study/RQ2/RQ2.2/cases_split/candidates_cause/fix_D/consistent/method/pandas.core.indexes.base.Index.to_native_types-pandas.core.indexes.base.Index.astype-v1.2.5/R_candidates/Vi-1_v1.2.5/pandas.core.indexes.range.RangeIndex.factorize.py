    def factorize(
        self, sort: bool = False, na_sentinel: Optional[int] = -1
    ) -> Tuple[np.ndarray, "RangeIndex"]:
        codes = np.arange(len(self), dtype=np.intp)
        uniques = self
        if sort and self.step < 0:
            codes = codes[::-1]
            uniques = uniques[::-1]
        return codes, uniques
