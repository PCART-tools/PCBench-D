    @doc(Index.duplicated)
    def duplicated(self, keep: DropKeep = "first") -> npt.NDArray[np.bool_]:
        shape = tuple(len(lev) for lev in self.levels)
        ids = get_group_index(self.codes, shape, sort=False, xnull=False)

        return duplicated(ids, keep)
