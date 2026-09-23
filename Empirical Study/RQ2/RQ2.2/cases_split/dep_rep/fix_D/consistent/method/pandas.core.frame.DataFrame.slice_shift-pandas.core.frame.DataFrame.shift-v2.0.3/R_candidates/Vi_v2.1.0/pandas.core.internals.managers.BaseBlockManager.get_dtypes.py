    def get_dtypes(self) -> npt.NDArray[np.object_]:
        dtypes = np.array([blk.dtype for blk in self.blocks], dtype=object)
        return dtypes.take(self.blknos)
