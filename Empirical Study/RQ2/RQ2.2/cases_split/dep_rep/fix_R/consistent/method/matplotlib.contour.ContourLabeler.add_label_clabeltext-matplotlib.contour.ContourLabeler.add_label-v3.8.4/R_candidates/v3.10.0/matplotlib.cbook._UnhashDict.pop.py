    def pop(self, key, *args):
        try:
            if key in self._dict:
                return self._dict.pop(key)
        except TypeError:
            for i, (k, v) in enumerate(self._pairs):
                if k == key:
                    del self._pairs[i]
                    return v
        if args:
            return args[0]
        raise KeyError(key)
