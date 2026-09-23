    def set_fontproperties(self, fp):
        """
        Set the font properties that control the text.  *fp* must be a
        :class:`matplotlib.font_manager.FontProperties` object.

        ACCEPTS: a :class:`matplotlib.font_manager.FontProperties` instance
        """
        if isinstance(fp, six.string_types):
            fp = FontProperties(fp)
        self._fontproperties = fp.copy()
        self.stale = True
