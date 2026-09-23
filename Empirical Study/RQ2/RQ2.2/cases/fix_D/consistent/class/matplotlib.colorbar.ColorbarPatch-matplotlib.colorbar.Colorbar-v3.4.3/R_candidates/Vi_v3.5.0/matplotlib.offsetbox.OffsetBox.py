class OffsetBox(martist.Artist):
    """
    The OffsetBox is a simple container artist.

    The child artists are meant to be drawn at a relative position to its
    parent.

    Being an artist itself, all parameters are passed on to `.Artist`.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.update(kwargs)
        # Clipping has not been implemented in the OffsetBox family, so
        # disable the clip flag for consistency. It can always be turned back
        # on to zero effect.
        self.set_clip_on(False)
        self._children = []
        self._offset = (0, 0)

    def set_figure(self, fig):
        """
        Set the `.Figure` for the `.OffsetBox` and all its children.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
        """
        super().set_figure(fig)
        for c in self.get_children():
            c.set_figure(fig)

    @martist.Artist.axes.setter
    def axes(self, ax):
        # TODO deal with this better
        martist.Artist.axes.fset(self, ax)
        for c in self.get_children():
            if c is not None:
                c.axes = ax

    def contains(self, mouseevent):
        """
        Delegate the mouse event contains-check to the children.

        As a container, the `.OffsetBox` does not respond itself to
        mouseevents.

        Parameters
        ----------
        mouseevent : `matplotlib.backend_bases.MouseEvent`

        Returns
        -------
        contains : bool
            Whether any values are within the radius.
        details : dict
            An artist-specific dictionary of details of the event context,
            such as which points are contained in the pick radius. See the
            individual Artist subclasses for details.

        See Also
        --------
        .Artist.contains
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        for c in self.get_children():
            a, b = c.contains(mouseevent)
            if a:
                return a, b
        return False, {}

    def set_offset(self, xy):
        """
        Set the offset.

        Parameters
        ----------
        xy : (float, float) or callable
            The (x, y) coordinates of the offset in display units. These can
            either be given explicitly as a tuple (x, y), or by providing a
            function that converts the extent into the offset. This function
            must have the signature::

                def offset(width, height, xdescent, ydescent, renderer) \
-> (float, float)
        """
        self._offset = xy
        self.stale = True

    def get_offset(self, width, height, xdescent, ydescent, renderer):
        """
        Return the offset as a tuple (x, y).

        The extent parameters have to be provided to handle the case where the
        offset is dynamically determined by a callable (see
        `~.OffsetBox.set_offset`).

        Parameters
        ----------
        width, height, xdescent, ydescent
            Extent parameters.
        renderer : `.RendererBase` subclass

        """
        return (self._offset(width, height, xdescent, ydescent, renderer)
                if callable(self._offset)
                else self._offset)

    def set_width(self, width):
        """
        Set the width of the box.

        Parameters
        ----------
        width : float
        """
        self.width = width
        self.stale = True

    def set_height(self, height):
        """
        Set the height of the box.

        Parameters
        ----------
        height : float
        """
        self.height = height
        self.stale = True

    def get_visible_children(self):
        r"""Return a list of the visible child `.Artist`\s."""
        return [c for c in self._children if c.get_visible()]

    def get_children(self):
        r"""Return a list of the child `.Artist`\s."""
        return self._children

    def get_extent_offsets(self, renderer):
        """
        Update offset of the children and return the extent of the box.

        Parameters
        ----------
        renderer : `.RendererBase` subclass

        Returns
        -------
        width
        height
        xdescent
        ydescent
        list of (xoffset, yoffset) pairs
        """
        raise NotImplementedError(
            "get_extent_offsets must be overridden in derived classes.")

    def get_extent(self, renderer):
        """Return a tuple ``width, height, xdescent, ydescent`` of the box."""
        w, h, xd, yd, offsets = self.get_extent_offsets(renderer)
        return w, h, xd, yd

    def get_window_extent(self, renderer):
        # docstring inherited
        w, h, xd, yd, offsets = self.get_extent_offsets(renderer)
        px, py = self.get_offset(w, h, xd, yd, renderer)
        return mtransforms.Bbox.from_bounds(px - xd, py - yd, w, h)

    def draw(self, renderer):
        """
        Update the location of children if necessary and draw them
        to the given *renderer*.
        """
        width, height, xdescent, ydescent, offsets = self.get_extent_offsets(
                                                        renderer)

        px, py = self.get_offset(width, height, xdescent, ydescent, renderer)

        for c, (ox, oy) in zip(self.get_visible_children(), offsets):
            c.set_offset((px + ox, py + oy))
            c.draw(renderer)

        bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
