    def get_dtypes(self):
        dtypes = np.array([blk.dtype for blk in self.blocks])
        return dtypes.take(self.blknos)
