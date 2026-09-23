    def set_norm(self, norm):
        if self._A is not None:
            raise RuntimeError('Cannot change colors after loading data')
        super(NonUniformImage, self).set_norm(norm)
