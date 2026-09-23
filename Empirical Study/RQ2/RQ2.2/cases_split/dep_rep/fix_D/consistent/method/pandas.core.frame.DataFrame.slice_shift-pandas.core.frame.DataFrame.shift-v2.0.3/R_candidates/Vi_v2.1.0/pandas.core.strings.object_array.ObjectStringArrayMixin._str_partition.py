    def _str_partition(self, sep: str, expand):
        result = self._str_map(lambda x: x.partition(sep), dtype="object")
        return result
