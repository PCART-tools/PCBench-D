    @_docstring.dedent_interpd
    @_api.make_keyword_only("3.6", name="mutation_scale")
    @_api.delete_parameter("3.4", "bbox_transmuter", alternative="boxstyle")
    def __init__(self, xy, width, height,
                 boxstyle="round", bbox_transmuter=None,
                 mutation_scale=1, mutation_aspect=1,
                 **kwargs):
        """
        Parameters
        ----------
        xy : float, float
          The lower left corner of the box.

        width : float
            The width of the box.

        height : float
            The height of the box.

        boxstyle : str or `matplotlib.patches.BoxStyle`
            The style of the fancy box. This can either be a `.BoxStyle`
            instance or a string of the style name and optionally comma
            separated attributes (e.g. "Round, pad=0.2"). This string is
            passed to `.BoxStyle` to construct a `.BoxStyle` object. See
            there for a full documentation.

            The following box styles are available:

            %(BoxStyle:table)s

        mutation_scale : float, default: 1
            Scaling factor applied to the attributes of the box style
            (e.g. pad or rounding_size).

        mutation_aspect : float, default: 1
            The height of the rectangle will be squeezed by this value before
            the mutation and the mutated box will be stretched by the inverse
            of it. For example, this allows different horizontal and vertical
            padding.

        Other Parameters
        ----------------
        **kwargs : `.Patch` properties

        %(Patch:kwdoc)s
        """

        super().__init__(**kwargs)

        self._x = xy[0]
        self._y = xy[1]
        self._width = width
        self._height = height

        if boxstyle == "custom":
            _api.warn_deprecated(
                "3.4", message="Support for boxstyle='custom' is deprecated "
                "since %(since)s and will be removed %(removal)s; directly "
                "pass a boxstyle instance as the boxstyle parameter instead.")
            if bbox_transmuter is None:
                raise ValueError("bbox_transmuter argument is needed with "
                                 "custom boxstyle")
            self._bbox_transmuter = bbox_transmuter
        else:
            self.set_boxstyle(boxstyle)

        self._mutation_scale = mutation_scale
        self._mutation_aspect = mutation_aspect

        self.stale = True
