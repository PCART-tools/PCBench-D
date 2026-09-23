    def _add_text(self, txt):
        """
        Add a `~.Text` to the axes' texts; return the text.
        """
        self._set_artist_props(txt)
        self.texts.append(txt)
        txt._remove_method = self.texts.remove
        self.stale = True
        return txt
