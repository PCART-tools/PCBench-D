    def get_sized_alternatives_for_symbol(self, fontname, sym):
        fixes = {'\\{': '{', '\\}': '}', '\\[': '[', '\\]': ']'}
        sym = fixes.get(sym, sym)

        alternatives = self._size_alternatives.get(sym)
        if alternatives:
            return alternatives

        alternatives = []
        try:
            uniindex = get_unicode_index(sym)
        except ValueError:
            return [(fontname, sym)]

        fix_ups = {
            ord('<'): 0x27e8,
            ord('>'): 0x27e9 }

        uniindex = fix_ups.get(uniindex, uniindex)

        for i in range(6):
            font = self._get_font(i)
            glyphindex = font.get_char_index(uniindex)
            if glyphindex != 0:
                alternatives.append((i, chr(uniindex)))

        # The largest size of the radical symbol in STIX has incorrect
        # metrics that cause it to be disconnected from the stem.
        if sym == r'\__sqrt__':
            alternatives = alternatives[:-1]

        self._size_alternatives[sym] = alternatives
        return alternatives
