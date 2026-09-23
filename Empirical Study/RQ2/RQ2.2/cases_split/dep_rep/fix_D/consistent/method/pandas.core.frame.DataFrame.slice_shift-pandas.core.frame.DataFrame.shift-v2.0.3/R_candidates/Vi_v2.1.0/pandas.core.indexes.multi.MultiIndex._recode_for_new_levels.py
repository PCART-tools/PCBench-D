    def _recode_for_new_levels(
        self, new_levels, copy: bool = True
    ) -> Generator[np.ndarray, None, None]:
        if len(new_levels) != self.nlevels:
            raise AssertionError(
                f"Length of new_levels ({len(new_levels)}) "
                f"must be same as self.nlevels ({self.nlevels})"
            )
        for i in range(self.nlevels):
            yield recode_for_categories(
                self.codes[i], self.levels[i], new_levels[i], copy=copy
            )
