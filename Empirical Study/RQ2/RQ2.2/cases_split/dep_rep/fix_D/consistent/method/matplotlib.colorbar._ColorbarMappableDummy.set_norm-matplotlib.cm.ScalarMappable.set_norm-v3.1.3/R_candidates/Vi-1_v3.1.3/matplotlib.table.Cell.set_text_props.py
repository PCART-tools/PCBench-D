    @docstring.dedent_interpd
    def set_text_props(self, **kwargs):
        """
        Update the text properties.

        Valid kwargs are
        %(Text)s
        """
        self._text.update(kwargs)
        self.stale = True
