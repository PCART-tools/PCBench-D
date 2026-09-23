    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            key = tuple(com._apply_if_callable(x, self.obj) for x in key)
        else:
            # scalar callable may return tuple
            key = com._apply_if_callable(key, self.obj)

        if not isinstance(key, tuple):
            key = self._tuplify(key)
        if len(key) != self.obj.ndim:
            raise ValueError('Not enough indexers for scalar access '
                             '(setting)!')
        key = list(self._convert_key(key, is_setter=True))
        key.append(value)
        self.obj.set_value(*key, takeable=self._takeable)
