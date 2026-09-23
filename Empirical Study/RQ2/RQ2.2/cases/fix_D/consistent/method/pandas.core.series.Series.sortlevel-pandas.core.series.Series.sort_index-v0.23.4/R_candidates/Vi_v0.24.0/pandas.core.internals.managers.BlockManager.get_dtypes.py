    def get_dtypes(self):
        dtypes = np.array([blk.dtype for blk in self.blocks])
        return algos.take_1d(dtypes, self._blknos, allow_fill=False)
