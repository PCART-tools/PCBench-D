    @docstring.dedent_interpd
    def set_marker(self, marker):
        """
        Set the line marker.

        Parameters
        ----------
        marker : marker style
            See `~matplotlib.markers` for full description of possible
            arguments.
        """
        self._marker.set_marker(marker)
        self.stale = True
