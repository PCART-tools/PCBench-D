    def __setitem__(self, key, value):
        super(_ColorMapping, self).__setitem__(key, value)
        self.cache.clear()
