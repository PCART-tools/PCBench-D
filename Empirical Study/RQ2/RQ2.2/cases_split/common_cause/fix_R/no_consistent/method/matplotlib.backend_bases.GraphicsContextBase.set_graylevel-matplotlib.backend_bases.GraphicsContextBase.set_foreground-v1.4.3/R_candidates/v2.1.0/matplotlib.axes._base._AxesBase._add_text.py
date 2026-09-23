    def _add_text(self, txt):
        """

        """
        self._set_artist_props(txt)
        self.texts.append(txt)
        txt._remove_method = lambda h: self.texts.remove(h)
        self.stale = True
        return txt
