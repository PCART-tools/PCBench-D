    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.slice(start=key.start, stop=key.stop,
                              step=key.step)
        else:
            return self.get(key)
