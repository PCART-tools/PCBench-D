    def get_box_aspect(self):
        """
        Get the axes box aspect.
        Will be ``None`` if not explicitly specified.

        See Also
        --------
        matplotlib.axes.Axes.set_box_aspect
            for a description of box aspect.
        matplotlib.axes.Axes.set_aspect
            for a description of aspect handling.
        """
        return self._box_aspect
