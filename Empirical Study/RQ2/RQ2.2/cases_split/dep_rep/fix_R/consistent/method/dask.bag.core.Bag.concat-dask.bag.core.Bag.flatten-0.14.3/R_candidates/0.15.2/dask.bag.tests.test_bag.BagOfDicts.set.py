    def set(self, key, value):
        def setter(d):
            d[key] = value
            return d
        return self.map(setter)
