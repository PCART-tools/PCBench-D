    def set_text(self, s):
        """
        Set the text string *s*

        It may contain newlines (``\\n``) or math in LaTeX syntax.

        ACCEPTS: string or anything printable with '%s' conversion.
        """
        self._text = '%s' % (s,)
        self.stale = True
