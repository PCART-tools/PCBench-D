    def add(self, key):
        self._od.pop(key, None)
        self._od[key] = None
