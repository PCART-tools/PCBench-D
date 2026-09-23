class Polygon(Patch):
    """A general polygon patch."""

    def __str__(self):
        if len(self._path.vertices):
            s = "Polygon%d((%g, %g) ...)"
            return s % (len(self._path.vertices), *self._path.vertices[0])
        else:
            return "Polygon0()"

    @docstring.dedent_interpd
    def __init__(self, xy, closed=True, **kwargs):
        """
        *xy* is a numpy array with shape Nx2.

        If *closed* is *True*, the polygon will be closed so the
        starting and ending points are the same.

        Valid keyword arguments are:

        %(Patch_kwdoc)s
        """
        super().__init__(**kwargs)
        self._closed = closed
        self.set_xy(xy)

    def get_path(self):
        """Get the `.Path` of the polygon."""
        return self._path

    def get_closed(self):
        """Return whether the polygon is closed."""
        return self._closed

    def set_closed(self, closed):
        """
        Set whether the polygon is closed.

        Parameters
        ----------
        closed : bool
           True if the polygon is closed
        """
        if self._closed == bool(closed):
            return
        self._closed = bool(closed)
        self.set_xy(self.get_xy())
        self.stale = True

    def get_xy(self):
        """
        Get the vertices of the path.

        Returns
        -------
        (N, 2) numpy array
            The coordinates of the vertices.
        """
        return self._path.vertices

    def set_xy(self, xy):
        """
        Set the vertices of the polygon.

        Parameters
        ----------
        xy : (N, 2) array-like
            The coordinates of the vertices.

        Notes
        -----
        Unlike `~.path.Path`, we do not ignore the last input vertex. If the
        polygon is meant to be closed, and the last point of the polygon is not
        equal to the first, we assume that the user has not explicitly passed a
        ``CLOSEPOLY`` vertex, and add it ourselves.
        """
        xy = np.asarray(xy)
        nverts, _ = xy.shape
        if self._closed:
            # if the first and last vertex are the "same", then we assume that
            # the user explicitly passed the CLOSEPOLY vertex. Otherwise, we
            # have to append one since the last vertex will be "ignored" by
            # Path
            if nverts == 1 or nverts > 1 and (xy[0] != xy[-1]).any():
                xy = np.concatenate([xy, [xy[0]]])
        else:
            # if we aren't closed, and the last vertex matches the first, then
            # we assume we have an unnecessary CLOSEPOLY vertex and remove it
            if nverts > 2 and (xy[0] == xy[-1]).all():
                xy = xy[:-1]
        self._path = Path(xy, closed=self._closed)
        self.stale = True

    xy = property(get_xy, set_xy,
                  doc='The vertices of the path as (N, 2) numpy array.')
