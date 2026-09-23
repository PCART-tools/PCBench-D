class PathPatch(Patch):
    """A general polycurve path patch."""

    _edge_default = True

    def __str__(self):
        s = "PathPatch%d((%g, %g) ...)"
        return s % (len(self._path.vertices), *tuple(self._path.vertices[0]))

    @docstring.dedent_interpd
    def __init__(self, path, **kwargs):
        """
        *path* is a `~.path.Path` object.

        Valid keyword arguments are:

        %(Patch:kwdoc)s
        """
        super().__init__(**kwargs)
        self._path = path

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path
