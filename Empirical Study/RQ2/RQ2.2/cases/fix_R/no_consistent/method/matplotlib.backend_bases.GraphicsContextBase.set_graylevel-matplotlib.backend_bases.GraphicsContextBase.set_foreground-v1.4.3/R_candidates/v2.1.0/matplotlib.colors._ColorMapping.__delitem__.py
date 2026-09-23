    def __delitem__(self, key):
        super(_ColorMapping, self).__delitem__(key)
        self.cache.clear()
