    def _str_rpartition(self, sep: str, expand):
        return self._str_map(lambda x: x.rpartition(sep), dtype="object")
