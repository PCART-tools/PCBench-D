    def set_fontproperties(self, fp):
        """
        Set the font properties that control the text.

        Parameters
        ----------
        fp : `.font_manager.FontProperties`
        """
        if isinstance(fp, str):
            fp = FontProperties(fp)
        self._fontproperties = fp.copy()
        self.stale = True
