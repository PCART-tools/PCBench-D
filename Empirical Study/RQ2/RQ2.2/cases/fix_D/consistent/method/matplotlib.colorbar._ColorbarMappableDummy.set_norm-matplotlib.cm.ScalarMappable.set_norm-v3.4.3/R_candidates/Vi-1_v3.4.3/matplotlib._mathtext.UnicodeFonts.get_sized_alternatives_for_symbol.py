    def get_sized_alternatives_for_symbol(self, fontname, sym):
        if self.cm_fallback:
            return self.cm_fallback.get_sized_alternatives_for_symbol(
                fontname, sym)
        return [(fontname, sym)]
