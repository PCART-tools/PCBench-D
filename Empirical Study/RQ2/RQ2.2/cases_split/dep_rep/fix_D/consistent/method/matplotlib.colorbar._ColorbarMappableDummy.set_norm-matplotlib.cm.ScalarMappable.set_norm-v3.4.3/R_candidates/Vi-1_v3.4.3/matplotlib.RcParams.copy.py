    def copy(self):
        return {k: dict.__getitem__(self, k) for k in self}
