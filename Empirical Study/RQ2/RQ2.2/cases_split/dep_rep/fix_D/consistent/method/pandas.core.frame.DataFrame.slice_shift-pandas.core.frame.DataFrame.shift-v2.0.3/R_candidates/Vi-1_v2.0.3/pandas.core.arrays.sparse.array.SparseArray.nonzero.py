    def nonzero(self) -> tuple[npt.NDArray[np.int32]]:
        if self.fill_value == 0:
            return (self.sp_index.indices,)
        else:
            return (self.sp_index.indices[self.sp_values != 0],)
