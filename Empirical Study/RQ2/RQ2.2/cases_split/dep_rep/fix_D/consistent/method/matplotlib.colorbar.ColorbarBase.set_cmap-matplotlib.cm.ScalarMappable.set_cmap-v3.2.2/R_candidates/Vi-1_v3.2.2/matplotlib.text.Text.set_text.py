    def set_text(self, s):
        r"""
        Set the text string *s*.

        It may contain newlines (``\n``) or math in LaTeX syntax.

        Parameters
        ----------
        s : object
            Any object gets converted to its `str`, except ``None`` which
            becomes ``''``.
        """
        if s is None:
            s = ''
        if s != self._text:
            self._text = str(s)
            self.stale = True
