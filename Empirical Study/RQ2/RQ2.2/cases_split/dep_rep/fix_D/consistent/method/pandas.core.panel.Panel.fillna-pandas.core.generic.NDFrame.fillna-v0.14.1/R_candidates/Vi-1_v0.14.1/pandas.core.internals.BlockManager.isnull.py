    def isnull(self, **kwargs):
        return self.apply('apply', **kwargs)
