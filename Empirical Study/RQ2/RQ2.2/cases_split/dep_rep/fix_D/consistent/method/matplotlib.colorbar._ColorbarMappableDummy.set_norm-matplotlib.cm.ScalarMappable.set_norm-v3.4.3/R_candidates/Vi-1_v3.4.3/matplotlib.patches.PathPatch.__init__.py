    @docstring.dedent_interpd
    def __init__(self, path, **kwargs):
        """
        *path* is a `~.path.Path` object.

        Valid keyword arguments are:

        %(Patch_kwdoc)s
        """
        super().__init__(**kwargs)
        self._path = path
