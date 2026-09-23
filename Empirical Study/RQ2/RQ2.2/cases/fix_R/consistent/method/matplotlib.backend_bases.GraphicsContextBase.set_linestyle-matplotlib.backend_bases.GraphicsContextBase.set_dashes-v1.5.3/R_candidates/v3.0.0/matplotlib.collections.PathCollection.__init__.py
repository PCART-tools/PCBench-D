    @docstring.dedent_interpd
    def __init__(self, paths, sizes=None, **kwargs):
        """
        *paths* is a sequence of :class:`matplotlib.path.Path`
        instances.

        %(Collection)s
        """

        Collection.__init__(self, **kwargs)
        self.set_paths(paths)
        self.set_sizes(sizes)
        self.stale = True
