    @property
    def sticky_edges(self):
        """
        `x` and `y` sticky edge lists.

        When performing autoscaling, if a data limit coincides with a value in
        the corresponding sticky_edges list, then no margin will be added--the
        view limit "sticks" to the edge. A typical usecase is histograms,
        where one usually expects no margin on the bottom edge (0) of the
        histogram.

        This attribute cannot be assigned to; however, the `x` and `y` lists
        can be modified in place as needed.

        Examples
        --------

        >>> artist.sticky_edges.x[:] = (xmin, xmax)
        >>> artist.sticky_edges.y[:] = (ymin, ymax)

        """
        return self._sticky_edges
