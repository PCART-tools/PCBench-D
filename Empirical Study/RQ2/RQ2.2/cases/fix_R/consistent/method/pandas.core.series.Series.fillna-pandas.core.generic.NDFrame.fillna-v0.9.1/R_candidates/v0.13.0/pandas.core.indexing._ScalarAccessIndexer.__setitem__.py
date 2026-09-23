    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            key = self._tuplify(key)
        if len(key) != self.obj.ndim:
            raise ValueError('Not enough indexers for scalar access '
                             '(setting)!')
        key = self._convert_key(key)
        key.append(value)
        self.obj.set_value(*key)
