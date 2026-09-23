    def __setitem__(self, key, value):
        try:
            self._dict[key] = value
        except TypeError:
            for i, (k, v) in enumerate(self._pairs):
                if k == key:
                    self._pairs[i] = (key, value)
                    break
            else:
                self._pairs.append((key, value))
