    @_docstring.dedent_interpd
    def __init__(self, path, **kwargs):
        """
        *path* is a `.Path` object.

        Valid keyword arguments are:

        %(Patch:kwdoc)s
        """
        super().__init__(**kwargs)
        self._path = path
