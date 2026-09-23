    @final
    def _duplicated(self, keep: DropKeep = "first") -> npt.NDArray[np.bool_]:
        return algorithms.duplicated(self._values, keep=keep)
