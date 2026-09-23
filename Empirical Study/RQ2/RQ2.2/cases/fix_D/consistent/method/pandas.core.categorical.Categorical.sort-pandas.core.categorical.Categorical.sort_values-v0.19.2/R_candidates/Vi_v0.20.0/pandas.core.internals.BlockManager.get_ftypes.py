    def get_ftypes(self):
        ftypes = np.array([blk.ftype for blk in self.blocks])
        return algos.take_1d(ftypes, self._blknos, allow_fill=False)
