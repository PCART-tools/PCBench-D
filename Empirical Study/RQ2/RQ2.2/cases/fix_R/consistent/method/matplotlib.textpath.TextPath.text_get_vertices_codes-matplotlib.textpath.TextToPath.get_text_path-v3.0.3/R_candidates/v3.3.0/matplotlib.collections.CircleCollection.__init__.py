    def __init__(self, sizes, **kwargs):
        """
        Parameters
        ----------
        sizes : float or array-like
            The area of each circle in points^2.
        **kwargs
            Forwarded to `.Collection`.
        """
        Collection.__init__(self, **kwargs)
        self.set_sizes(sizes)
        self.set_transform(transforms.IdentityTransform())
        self._paths = [mpath.Path.unit_circle()]
