    @doc(Index.duplicated)
    def duplicated(self, keep="first") -> np.ndarray:
        shape = tuple(len(lev) for lev in self.levels)
        ids = get_group_index(self.codes, shape, sort=False, xnull=False)

        return duplicated(ids, keep)
