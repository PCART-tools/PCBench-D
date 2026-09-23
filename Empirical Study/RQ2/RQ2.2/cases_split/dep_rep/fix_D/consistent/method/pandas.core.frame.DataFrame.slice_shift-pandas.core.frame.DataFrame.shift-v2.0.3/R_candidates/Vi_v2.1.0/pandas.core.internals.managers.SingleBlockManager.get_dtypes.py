    def get_dtypes(self) -> npt.NDArray[np.object_]:
        return np.array([self._block.dtype], dtype=object)
