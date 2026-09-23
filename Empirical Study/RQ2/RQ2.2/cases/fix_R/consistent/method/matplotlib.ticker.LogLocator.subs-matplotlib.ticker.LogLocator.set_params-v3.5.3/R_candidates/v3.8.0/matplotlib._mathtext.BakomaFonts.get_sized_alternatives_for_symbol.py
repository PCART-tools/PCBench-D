    def get_sized_alternatives_for_symbol(self, fontname: str,
                                          sym: str) -> list[tuple[str, str]]:
        return self._size_alternatives.get(sym, [(fontname, sym)])
