    @property
    def nbytes(self):
        return self.sp_values.nbytes + self.sp_index.nbytes
