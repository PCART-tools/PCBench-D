    def _str_rpartition(self, sep, expand):
        return self._str_map(lambda x: x.rpartition(sep), dtype="object")
