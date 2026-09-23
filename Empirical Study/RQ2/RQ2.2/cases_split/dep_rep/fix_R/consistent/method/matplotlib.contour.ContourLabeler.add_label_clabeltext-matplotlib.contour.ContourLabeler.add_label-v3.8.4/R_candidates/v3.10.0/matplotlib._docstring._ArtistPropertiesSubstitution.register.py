    def register(self, **kwargs):
        """
        Register substitutions.

        ``_docstring.interpd.register(name="some value")`` makes "name" available
        as a named parameter that will be replaced by "some value".
        """
        self.params.update(**kwargs)
