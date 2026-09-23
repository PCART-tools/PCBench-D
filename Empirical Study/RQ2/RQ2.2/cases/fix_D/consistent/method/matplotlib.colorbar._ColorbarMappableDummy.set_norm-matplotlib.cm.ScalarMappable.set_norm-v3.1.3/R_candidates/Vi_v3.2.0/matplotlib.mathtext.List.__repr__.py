    def __repr__(self):
        return '[%s <%.02f %.02f %.02f %.02f> %s]' % (
            super().__repr__(),
            self.width, self.height,
            self.depth, self.shift_amount,
            ' '.join([repr(x) for x in self.children]))
