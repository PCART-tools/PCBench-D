    def _char_index_at(self, x):
        """
        Calculate the index closest to the coordinate x in display space.

        The position of text[index] is assumed to be the sum of the widths
        of all preceding characters text[:index].

        This works only on single line texts.
        """
        if not self._text:
            return 0

        text = self._text

        fontproperties = str(self._fontproperties)
        if fontproperties not in Text._charsize_cache:
            Text._charsize_cache[fontproperties] = dict()

        charsize_cache = Text._charsize_cache[fontproperties]
        for char in set(text):
            if char not in charsize_cache:
                self.set_text(char)
                bb = self.get_window_extent()
                charsize_cache[char] = bb.x1 - bb.x0

        self.set_text(text)
        bb = self.get_window_extent()

        size_accum = np.cumsum([0] + [charsize_cache[x] for x in text])
        std_x = x - bb.x0
        return (np.abs(size_accum - std_x)).argmin()
