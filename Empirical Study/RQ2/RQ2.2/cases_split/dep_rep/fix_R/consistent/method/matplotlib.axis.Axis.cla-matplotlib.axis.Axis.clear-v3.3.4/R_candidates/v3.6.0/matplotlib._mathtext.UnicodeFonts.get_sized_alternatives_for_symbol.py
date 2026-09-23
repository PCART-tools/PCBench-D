    def get_sized_alternatives_for_symbol(self, fontname, sym):
        if self._fallback_font:
            return self._fallback_font.get_sized_alternatives_for_symbol(
                fontname, sym)
        return [(fontname, sym)]
