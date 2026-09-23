    def get_box_aspect(self):
        """
        Return the axes box aspect, i.e. the ratio of height to width.

        The box aspect is ``None`` (i.e. chosen depending on the available
        figure space) unless explicitly specified.

        See Also
        --------
        matplotlib.axes.Axes.set_box_aspect
            for a description of box aspect.
        matplotlib.axes.Axes.set_aspect
            for a description of aspect handling.
        """
        return self._box_aspect
