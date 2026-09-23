    @docstring.dedent_interpd
    def __init__(self, sizes, **kwargs):
        """
        *sizes*
            Gives the area of the circle in points^2

        %(Collection)s
        """
        Collection.__init__(self, **kwargs)
        self.set_sizes(sizes)
        self.set_transform(transforms.IdentityTransform())
        self._paths = [mpath.Path.unit_circle()]
