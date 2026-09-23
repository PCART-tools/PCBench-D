    def set_variation_by_name(self, name):
        """
        :param name: The name of the style.
        :exception OSError: If the font is not a variation font.
        """
        names = self.get_variation_names()
        if not isinstance(name, bytes):
            name = name.encode()
        index = names.index(name) + 1

        if index == getattr(self, "_last_variation_index", None):
            # When the same name is set twice in a row,
            # there is an 'unknown freetype error'
            # https://savannah.nongnu.org/bugs/?56186
            return
        self._last_variation_index = index

        self.font.setvarname(index)
