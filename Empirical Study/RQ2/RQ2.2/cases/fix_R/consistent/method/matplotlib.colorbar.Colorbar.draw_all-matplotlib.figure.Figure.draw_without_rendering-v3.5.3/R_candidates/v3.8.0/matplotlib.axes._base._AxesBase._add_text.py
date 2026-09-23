    def _add_text(self, txt):
        """
        Add a `.Text` to the Axes; return the text.
        """
        _api.check_isinstance(mtext.Text, txt=txt)
        self._set_artist_props(txt)
        self._children.append(txt)
        txt._remove_method = self._children.remove
        self.stale = True
        return txt
