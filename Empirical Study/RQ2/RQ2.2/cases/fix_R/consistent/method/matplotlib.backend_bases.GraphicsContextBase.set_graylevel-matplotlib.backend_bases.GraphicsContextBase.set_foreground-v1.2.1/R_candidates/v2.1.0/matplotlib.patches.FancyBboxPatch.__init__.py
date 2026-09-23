    @docstring.dedent_interpd
    def __init__(self, xy, width, height,
                 boxstyle="round",
                 bbox_transmuter=None,
                 mutation_scale=1.,
                 mutation_aspect=None,
                 **kwargs):
        """
        *xy* = lower left corner

        *width*, *height*

        *boxstyle* determines what kind of fancy box will be drawn. It
        can be a string of the style name with a comma separated
        attribute, or an instance of :class:`BoxStyle`. Following box
        styles are available.

        %(AvailableBoxstyles)s

        *mutation_scale* : a value with which attributes of boxstyle
        (e.g., pad) will be scaled. default=1.

        *mutation_aspect* : The height of the rectangle will be
        squeezed by this value before the mutation and the mutated
        box will be stretched by the inverse of it. default=None.

        Valid kwargs are:
        %(Patch)s
        """

        Patch.__init__(self, **kwargs)

        self._x = xy[0]
        self._y = xy[1]
        self._width = width
        self._height = height

        if boxstyle == "custom":
            if bbox_transmuter is None:
                raise ValueError("bbox_transmuter argument is needed with "
                                 "custom boxstyle")
            self._bbox_transmuter = bbox_transmuter
        else:
            self.set_boxstyle(boxstyle)

        self._mutation_scale = mutation_scale
        self._mutation_aspect = mutation_aspect

        self.stale = True
