    @_docstring.interpd
    def set_text_props(self, **kwargs):
        """
        Update the text properties.

        Valid keyword arguments are:

        %(Text:kwdoc)s
        """
        self._text._internal_update(kwargs)
        self.stale = True
