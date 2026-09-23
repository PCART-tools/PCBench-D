    @property
    def verts(self):
        """Get the polygon vertices.

        Returns
        -------
        list
            A list of the vertices of the polygon as ``(xdata, ydata)`` tuples.
        """
        return list(zip(self._xs[:-1], self._ys[:-1]))
