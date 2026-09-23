    @final
    def _duplicated(
        self, keep: Literal["first", "last", False] = "first"
    ) -> npt.NDArray[np.bool_]:
        return duplicated(self._values, keep=keep)
