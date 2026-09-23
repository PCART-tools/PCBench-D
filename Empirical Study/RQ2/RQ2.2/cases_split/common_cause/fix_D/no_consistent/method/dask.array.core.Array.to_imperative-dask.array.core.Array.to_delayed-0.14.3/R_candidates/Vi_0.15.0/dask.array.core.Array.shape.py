    @property
    def shape(self):
        return tuple(map(sum, self.chunks))
