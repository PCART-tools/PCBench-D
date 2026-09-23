    def _str_strip(self, to_strip=None):
        return self._str_map(lambda x: x.strip(to_strip))
