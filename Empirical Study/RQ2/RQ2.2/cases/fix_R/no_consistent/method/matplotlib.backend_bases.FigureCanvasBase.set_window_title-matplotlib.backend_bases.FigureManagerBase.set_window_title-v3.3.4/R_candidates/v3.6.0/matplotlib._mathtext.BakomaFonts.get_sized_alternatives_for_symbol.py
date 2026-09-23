    def get_sized_alternatives_for_symbol(self, fontname, sym):
        return self._size_alternatives.get(sym, [(fontname, sym)])
