    @docstring.dedent_interpd
    def arrow(self, x, y, dx, dy, **kwargs):
        """
        Add an arrow to the axes.

        This draws an arrow from ``(x, y)`` to ``(x+dx, y+dy)``.

        Parameters
        ----------
        x, y : float
            The x and y coordinates of the arrow base.
        dx, dy : float
            The length of the arrow along x and y direction.

        Returns
        -------
        arrow : `.FancyArrow`
            The created `.FancyArrow` object.

        Other Parameters
        ----------------
        **kwargs
            Optional kwargs (inherited from `.FancyArrow` patch) control the
            arrow construction and properties:

        %(FancyArrow)s

        Notes
        -----
        The resulting arrow is affected by the axes aspect ratio and limits.
        This may produce an arrow whose head is not square with its stem. To
        create an arrow whose head is square with its stem,
        use :meth:`annotate` for example:

        >>> ax.annotate("", xy=(0.5, 0.5), xytext=(0, 0),
        ...             arrowprops=dict(arrowstyle="->"))

        """
        # Strip away units for the underlying patch since units
        # do not make sense to most patch-like code
        x = self.convert_xunits(x)
        y = self.convert_yunits(y)
        dx = self.convert_xunits(dx)
        dy = self.convert_yunits(dy)

        a = mpatches.FancyArrow(x, y, dx, dy, **kwargs)
        self.add_artist(a)
        return a
