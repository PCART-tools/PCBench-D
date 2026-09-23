    @docstring.dedent_interpd
    def __init__(self, path, **kwargs):
        """
        *path* is a :class:`matplotlib.path.Path` object.

        Valid kwargs are:
        %(Patch)s

        .. seealso::

            :class:`Patch`
                For additional kwargs

        """
        Patch.__init__(self, **kwargs)
        self._path = path
