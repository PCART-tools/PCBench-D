    def __repr__(self):
        return '%s<w=%.02f h=%.02f d=%.02f s=%.02f>[%s]' % (
            super().__repr__(),
            self.width, self.height,
            self.depth, self.shift_amount,
            ', '.join([repr(x) for x in self.children]))
