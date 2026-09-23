    def is_dropsub(self, nucleus):
        if isinstance(nucleus, Char):
            return nucleus.c in self._dropsub_symbols
        return False
