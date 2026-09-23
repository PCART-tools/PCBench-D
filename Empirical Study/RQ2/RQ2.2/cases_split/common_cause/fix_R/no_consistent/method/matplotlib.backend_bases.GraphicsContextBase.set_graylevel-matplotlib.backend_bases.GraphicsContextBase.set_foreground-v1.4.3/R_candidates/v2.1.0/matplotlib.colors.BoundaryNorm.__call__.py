    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        xx, is_scalar = self.process_value(value)
        mask = np.ma.getmaskarray(xx)
        xx = np.atleast_1d(xx.filled(self.vmax + 1))
        if clip:
            np.clip(xx, self.vmin, self.vmax, out=xx)
            max_col = self.Ncmap - 1
        else:
            max_col = self.Ncmap
        iret = np.zeros(xx.shape, dtype=np.int16)
        for i, b in enumerate(self.boundaries):
            iret[xx >= b] = i
        if self._interp:
            scalefac = float(self.Ncmap - 1) / (self.N - 2)
            iret = (iret * scalefac).astype(np.int16)
        iret[xx < self.vmin] = -1
        iret[xx >= self.vmax] = max_col
        ret = np.ma.array(iret, mask=mask)
        if is_scalar:
            ret = int(ret[0])  # assume python scalar
        return ret
