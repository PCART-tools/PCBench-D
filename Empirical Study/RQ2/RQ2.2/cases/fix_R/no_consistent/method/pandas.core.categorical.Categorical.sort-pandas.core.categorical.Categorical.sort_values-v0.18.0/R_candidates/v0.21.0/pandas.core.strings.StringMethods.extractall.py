    @copy(str_extractall)
    def extractall(self, pat, flags=0):
        return str_extractall(self._orig, pat, flags=flags)
