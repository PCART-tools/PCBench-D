    def __iter__(self):
        i = 0
        g = self.get(i)
        while g.notna().any():
            yield g
            i += 1
            g = self.get(i)
