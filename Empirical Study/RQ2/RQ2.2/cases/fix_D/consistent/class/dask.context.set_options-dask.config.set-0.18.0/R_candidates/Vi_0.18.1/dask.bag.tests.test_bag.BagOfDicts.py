class BagOfDicts(db.Bag):
    def get(self, key, default=None):
        return self.map(lambda d: d.get(key, default))

    def set(self, key, value):
        def setter(d):
            d[key] = value
            return d
        return self.map(setter)
