    def _strmap(self, key, *args, **kwargs):
        return self._bag.map(lambda s: getattr(s, key)(*args, **kwargs))
