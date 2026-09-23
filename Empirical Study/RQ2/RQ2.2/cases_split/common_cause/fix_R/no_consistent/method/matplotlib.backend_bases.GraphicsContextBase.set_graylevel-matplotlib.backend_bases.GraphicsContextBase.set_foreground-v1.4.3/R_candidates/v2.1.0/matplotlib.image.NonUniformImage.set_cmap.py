    def set_cmap(self, cmap):
        if self._A is not None:
            raise RuntimeError('Cannot change colors after loading data')
        super(NonUniformImage, self).set_cmap(cmap)
