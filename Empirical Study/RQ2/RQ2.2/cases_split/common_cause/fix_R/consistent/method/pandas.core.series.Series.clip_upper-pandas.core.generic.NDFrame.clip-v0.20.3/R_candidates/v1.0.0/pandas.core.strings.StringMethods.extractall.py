    @copy(str_extractall)
    @forbid_nonstring_types(["bytes"])
    def extractall(self, pat, flags=0):
        return str_extractall(self._orig, pat, flags=flags)
