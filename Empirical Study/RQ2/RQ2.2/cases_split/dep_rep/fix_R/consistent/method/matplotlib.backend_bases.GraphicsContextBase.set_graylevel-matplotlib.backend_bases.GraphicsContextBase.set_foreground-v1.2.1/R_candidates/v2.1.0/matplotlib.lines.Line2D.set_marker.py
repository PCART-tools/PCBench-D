    @docstring.dedent_interpd
    def set_marker(self, marker):
        """
        Set the line marker

        ACCEPTS: :mod:`A valid marker style <matplotlib.markers>`

        Parameters
        ----------

        marker: marker style
            See `~matplotlib.markers` for full description of possible
            argument

        """
        self._marker.set_marker(marker)
        self.stale = True
