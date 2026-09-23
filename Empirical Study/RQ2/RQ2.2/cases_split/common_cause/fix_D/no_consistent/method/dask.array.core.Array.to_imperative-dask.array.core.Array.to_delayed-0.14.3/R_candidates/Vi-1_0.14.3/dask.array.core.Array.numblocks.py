    @property
    def numblocks(self):
        return tuple(map(len, self.chunks))
