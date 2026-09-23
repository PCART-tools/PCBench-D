    def __repr__(self) -> str:
        return '{}<w={:.02f} h={:.02f} d={:.02f} s={:.02f}>[{}]'.format(
            super().__repr__(),
            self.width, self.height,
            self.depth, self.shift_amount,
            ', '.join([repr(x) for x in self.children]))
