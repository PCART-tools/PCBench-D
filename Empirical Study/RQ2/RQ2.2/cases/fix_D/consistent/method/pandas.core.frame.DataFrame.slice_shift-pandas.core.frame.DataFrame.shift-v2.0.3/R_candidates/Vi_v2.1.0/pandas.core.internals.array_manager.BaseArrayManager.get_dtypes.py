    def get_dtypes(self) -> npt.NDArray[np.object_]:
        return np.array([arr.dtype for arr in self.arrays], dtype="object")
