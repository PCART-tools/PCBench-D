    def __iter__(self):
        return iter(set(self._tagdata) | set(self._tags_v2))
