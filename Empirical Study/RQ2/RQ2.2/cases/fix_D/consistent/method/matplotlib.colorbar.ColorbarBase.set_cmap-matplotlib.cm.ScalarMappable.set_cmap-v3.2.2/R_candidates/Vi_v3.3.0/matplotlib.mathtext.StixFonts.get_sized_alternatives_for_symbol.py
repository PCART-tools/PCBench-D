    @functools.lru_cache()
    def get_sized_alternatives_for_symbol(self, fontname, sym):
        fixes = {
            '\\{': '{', '\\}': '}', '\\[': '[', '\\]': ']',
            '<': '\N{MATHEMATICAL LEFT ANGLE BRACKET}',
            '>': '\N{MATHEMATICAL RIGHT ANGLE BRACKET}',
        }
        sym = fixes.get(sym, sym)
        try:
            uniindex = get_unicode_index(sym)
        except ValueError:
            return [(fontname, sym)]
        alternatives = [(i, chr(uniindex)) for i in range(6)
                        if self._get_font(i).get_char_index(uniindex) != 0]
        # The largest size of the radical symbol in STIX has incorrect
        # metrics that cause it to be disconnected from the stem.
        if sym == r'\__sqrt__':
            alternatives = alternatives[:-1]
        return alternatives
