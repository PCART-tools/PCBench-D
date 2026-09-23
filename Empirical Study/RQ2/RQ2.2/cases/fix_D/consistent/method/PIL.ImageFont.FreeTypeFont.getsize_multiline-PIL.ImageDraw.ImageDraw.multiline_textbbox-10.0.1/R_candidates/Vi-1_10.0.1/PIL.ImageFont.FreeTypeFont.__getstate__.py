    def __getstate__(self):
        return [self.path, self.size, self.index, self.encoding, self.layout_engine]
