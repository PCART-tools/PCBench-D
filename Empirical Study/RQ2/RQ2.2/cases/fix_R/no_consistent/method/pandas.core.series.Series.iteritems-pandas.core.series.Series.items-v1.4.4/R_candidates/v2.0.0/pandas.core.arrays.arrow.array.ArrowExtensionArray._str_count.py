    def _str_count(self, pat: str, flags: int = 0):
        if flags:
            raise NotImplementedError(f"count not implemented with {flags=}")
        return type(self)(pc.count_substring_regex(self._data, pat))
