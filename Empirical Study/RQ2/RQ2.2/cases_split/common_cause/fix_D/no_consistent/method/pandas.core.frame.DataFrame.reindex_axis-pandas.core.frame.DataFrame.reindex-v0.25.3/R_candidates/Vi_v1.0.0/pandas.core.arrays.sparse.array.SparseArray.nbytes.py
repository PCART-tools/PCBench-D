    @property
    def nbytes(self) -> int:
        return self.sp_values.nbytes + self.sp_index.nbytes
