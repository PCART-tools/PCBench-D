    def __delitem__(self, key):
        super().__delitem__(key)
        self.cache.clear()
