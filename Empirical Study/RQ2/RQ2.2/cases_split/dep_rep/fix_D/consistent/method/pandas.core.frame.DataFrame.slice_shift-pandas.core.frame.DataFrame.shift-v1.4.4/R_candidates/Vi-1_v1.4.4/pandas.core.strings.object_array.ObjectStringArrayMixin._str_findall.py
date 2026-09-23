    def _str_findall(self, pat, flags=0):
        regex = re.compile(pat, flags=flags)
        return self._str_map(regex.findall, dtype="object")
