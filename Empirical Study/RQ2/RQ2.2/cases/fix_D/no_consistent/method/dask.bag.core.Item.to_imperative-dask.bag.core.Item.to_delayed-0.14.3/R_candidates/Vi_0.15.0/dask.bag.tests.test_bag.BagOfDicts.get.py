    def get(self, key, default=None):
        return self.map(lambda d: d.get(key, default))
