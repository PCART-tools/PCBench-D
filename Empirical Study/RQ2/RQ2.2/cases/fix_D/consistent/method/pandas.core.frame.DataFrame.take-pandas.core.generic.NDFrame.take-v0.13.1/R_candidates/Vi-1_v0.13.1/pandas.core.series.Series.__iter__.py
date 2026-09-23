    def __iter__(self):
        if np.issubdtype(self.dtype, np.datetime64):
            return (lib.Timestamp(x) for x in self.values)
        else:
            return iter(self.values)
