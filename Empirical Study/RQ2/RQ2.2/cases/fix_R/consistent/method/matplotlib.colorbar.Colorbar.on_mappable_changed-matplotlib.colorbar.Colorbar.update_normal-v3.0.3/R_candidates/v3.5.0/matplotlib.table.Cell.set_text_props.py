    @docstring.dedent_interpd
    def set_text_props(self, **kwargs):
        """
        Update the text properties.

        Valid keyword arguments are:

        %(Text:kwdoc)s
        """
        self._text.update(kwargs)
        self.stale = True
