    def set_text(self, s):
        "Set the text of this area as a string."
        self._text.set_text(s)
        self.stale = True
