    def set_text(self, s):
        """
        Set the text string *s*.

        It may contain newlines (``\\n``) or math in LaTeX syntax.

        Parameters
        ----------
        s : string or object castable to string (but ``None`` becomes ``''``)
        """
        if s is None:
            s = ''
        if s != self._text:
            self._text = '%s' % (s,)
            self.stale = True
