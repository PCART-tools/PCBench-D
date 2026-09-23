class FancyArrowPatch(Patch):
    """
    A fancy arrow patch. It draws an arrow using the `ArrowStyle`.

    The head and tail positions are fixed at the specified start and end points
    of the arrow, but the size and shape (in display coordinates) of the arrow
    does not change when the axis is moved or zoomed.
    """
    _edge_default = True

    def __str__(self):
        if self._posA_posB is not None:
            (x1, y1), (x2, y2) = self._posA_posB
            return f"{type(self).__name__}(({x1:g}, {y1:g})->({x2:g}, {y2:g}))"
        else:
            return f"{type(self).__name__}({self._path_original})"

    @docstring.dedent_interpd
    @_api.delete_parameter("3.4", "dpi_cor")
    def __init__(self, posA=None, posB=None, path=None,
                 arrowstyle="simple", connectionstyle="arc3",
                 patchA=None, patchB=None,
                 shrinkA=2, shrinkB=2,
                 mutation_scale=1, mutation_aspect=1,
                 dpi_cor=1,
                 **kwargs):
        """
        There are two ways for defining an arrow:

        - If *posA* and *posB* are given, a path connecting two points is
          created according to *connectionstyle*. The path will be
          clipped with *patchA* and *patchB* and further shrunken by
          *shrinkA* and *shrinkB*. An arrow is drawn along this
          resulting path using the *arrowstyle* parameter.

        - Alternatively if *path* is provided, an arrow is drawn along this
          path and *patchA*, *patchB*, *shrinkA*, and *shrinkB* are ignored.

        Parameters
        ----------
        posA, posB : (float, float), default: None
            (x, y) coordinates of arrow tail and arrow head respectively.

        path : `~matplotlib.path.Path`, default: None
            If provided, an arrow is drawn along this path and *patchA*,
            *patchB*, *shrinkA*, and *shrinkB* are ignored.

        arrowstyle : str or `.ArrowStyle`, default: 'simple'
            The `.ArrowStyle` with which the fancy arrow is drawn.  If a
            string, it should be one of the available arrowstyle names, with
            optional comma-separated attributes.  The optional attributes are
            meant to be scaled with the *mutation_scale*.  The following arrow
            styles are available:

            %(AvailableArrowstyles)s

        connectionstyle : str or `.ConnectionStyle` or None, optional, \
default: 'arc3'
            The `.ConnectionStyle` with which *posA* and *posB* are connected.
            If a string, it should be one of the available connectionstyle
            names, with optional comma-separated attributes.  The following
            connection styles are available:

            %(AvailableConnectorstyles)s

        patchA, patchB : `.Patch`, default: None
            Head and tail patches, respectively.

        shrinkA, shrinkB : float, default: 2
            Shrinking factor of the tail and head of the arrow respectively.

        mutation_scale : float, default: 1
            Value with which attributes of *arrowstyle* (e.g., *head_length*)
            will be scaled.

        mutation_aspect : None or float, default: None
            The height of the rectangle will be squeezed by this value before
            the mutation and the mutated box will be stretched by the inverse
            of it.

        dpi_cor : float, default: 1
            dpi_cor is currently used for linewidth-related things and shrink
            factor. Mutation scale is affected by this.  Deprecated.

        Other Parameters
        ----------------
        **kwargs : `.Patch` properties, optional
            Here is a list of available `.Patch` properties:

        %(Patch_kwdoc)s

            In contrast to other patches, the default ``capstyle`` and
            ``joinstyle`` for `FancyArrowPatch` are set to ``"round"``.
        """
        # Traditionally, the cap- and joinstyle for FancyArrowPatch are round
        kwargs.setdefault("joinstyle", JoinStyle.round)
        kwargs.setdefault("capstyle", CapStyle.round)

        super().__init__(**kwargs)

        if posA is not None and posB is not None and path is None:
            self._posA_posB = [posA, posB]

            if connectionstyle is None:
                connectionstyle = "arc3"
            self.set_connectionstyle(connectionstyle)

        elif posA is None and posB is None and path is not None:
            self._posA_posB = None
        else:
            raise ValueError("Either posA and posB, or path need to provided")

        self.patchA = patchA
        self.patchB = patchB
        self.shrinkA = shrinkA
        self.shrinkB = shrinkB

        self._path_original = path

        self.set_arrowstyle(arrowstyle)

        self._mutation_scale = mutation_scale
        self._mutation_aspect = mutation_aspect

        self._dpi_cor = dpi_cor

    @_api.deprecated("3.4")
    def set_dpi_cor(self, dpi_cor):
        """
        dpi_cor is currently used for linewidth-related things and
        shrink factor. Mutation scale is affected by this.

        Parameters
        ----------
        dpi_cor : float
        """
        self._dpi_cor = dpi_cor
        self.stale = True

    @_api.deprecated("3.4")
    def get_dpi_cor(self):
        """
        dpi_cor is currently used for linewidth-related things and
        shrink factor. Mutation scale is affected by this.

        Returns
        -------
        scalar
        """
        return self._dpi_cor

    def set_positions(self, posA, posB):
        """
        Set the begin and end positions of the connecting path.

        Parameters
        ----------
        posA, posB : None, tuple
            (x, y) coordinates of arrow tail and arrow head respectively. If
            `None` use current value.
        """
        if posA is not None:
            self._posA_posB[0] = posA
        if posB is not None:
            self._posA_posB[1] = posB
        self.stale = True

    def set_patchA(self, patchA):
        """
        Set the tail patch.

        Parameters
        ----------
        patchA : `.patches.Patch`
        """
        self.patchA = patchA
        self.stale = True

    def set_patchB(self, patchB):
        """
        Set the head patch.

        Parameters
        ----------
        patchB : `.patches.Patch`
        """
        self.patchB = patchB
        self.stale = True

    def set_connectionstyle(self, connectionstyle, **kw):
        """
        Set the connection style. Old attributes are forgotten.

        Parameters
        ----------
        connectionstyle : str or `.ConnectionStyle` or None, optional
            Can be a string with connectionstyle name with
            optional comma-separated attributes, e.g.::

                set_connectionstyle("arc,angleA=0,armA=30,rad=10")

            Alternatively, the attributes can be provided as keywords, e.g.::

                set_connectionstyle("arc", angleA=0,armA=30,rad=10)

            Without any arguments (or with ``connectionstyle=None``), return
            available styles as a list of strings.
        """

        if connectionstyle is None:
            return ConnectionStyle.pprint_styles()

        if (isinstance(connectionstyle, ConnectionStyle._Base) or
                callable(connectionstyle)):
            self._connector = connectionstyle
        else:
            self._connector = ConnectionStyle(connectionstyle, **kw)
        self.stale = True

    def get_connectionstyle(self):
        """Return the `ConnectionStyle` used."""
        return self._connector

    def set_arrowstyle(self, arrowstyle=None, **kw):
        """
        Set the arrow style. Old attributes are forgotten. Without arguments
        (or with ``arrowstyle=None``) returns available box styles as a list of
        strings.

        Parameters
        ----------
        arrowstyle : None or ArrowStyle or str, default: None
            Can be a string with arrowstyle name with optional comma-separated
            attributes, e.g.::

                set_arrowstyle("Fancy,head_length=0.2")

            Alternatively attributes can be provided as keywords, e.g.::

                set_arrowstyle("fancy", head_length=0.2)

        """

        if arrowstyle is None:
            return ArrowStyle.pprint_styles()

        if isinstance(arrowstyle, ArrowStyle._Base):
            self._arrow_transmuter = arrowstyle
        else:
            self._arrow_transmuter = ArrowStyle(arrowstyle, **kw)
        self.stale = True

    def get_arrowstyle(self):
        """Return the arrowstyle object."""
        return self._arrow_transmuter

    def set_mutation_scale(self, scale):
        """
        Set the mutation scale.

        Parameters
        ----------
        scale : float
        """
        self._mutation_scale = scale
        self.stale = True

    def get_mutation_scale(self):
        """
        Return the mutation scale.

        Returns
        -------
        scalar
        """
        return self._mutation_scale

    def set_mutation_aspect(self, aspect):
        """
        Set the aspect ratio of the bbox mutation.

        Parameters
        ----------
        aspect : float
        """
        self._mutation_aspect = aspect
        self.stale = True

    def get_mutation_aspect(self):
        """Return the aspect ratio of the bbox mutation."""
        return (self._mutation_aspect if self._mutation_aspect is not None
                else 1)  # backcompat.

    def get_path(self):
        """
        Return the path of the arrow in the data coordinates. Use
        get_path_in_displaycoord() method to retrieve the arrow path
        in display coordinates.
        """
        _path, fillable = self.get_path_in_displaycoord()
        if np.iterable(fillable):
            _path = Path.make_compound_path(*_path)
        return self.get_transform().inverted().transform_path(_path)

    def get_path_in_displaycoord(self):
        """Return the mutated path of the arrow in display coordinates."""
        dpi_cor = self._dpi_cor

        if self._posA_posB is not None:
            posA = self._convert_xy_units(self._posA_posB[0])
            posB = self._convert_xy_units(self._posA_posB[1])
            (posA, posB) = self.get_transform().transform((posA, posB))
            _path = self.get_connectionstyle()(posA, posB,
                                               patchA=self.patchA,
                                               patchB=self.patchB,
                                               shrinkA=self.shrinkA * dpi_cor,
                                               shrinkB=self.shrinkB * dpi_cor
                                               )
        else:
            _path = self.get_transform().transform_path(self._path_original)

        _path, fillable = self.get_arrowstyle()(
            _path,
            self.get_mutation_scale() * dpi_cor,
            self.get_linewidth() * dpi_cor,
            self.get_mutation_aspect())

        return _path, fillable

    def draw(self, renderer):
        if not self.get_visible():
            return

        with self._bind_draw_path_function(renderer) as draw_path:

            # FIXME : dpi_cor is for the dpi-dependency of the linewidth. There
            # could be room for improvement.  Maybe get_path_in_displaycoord
            # could take a renderer argument, but get_path should be adapted
            # too.
            self._dpi_cor = renderer.points_to_pixels(1.)
            path, fillable = self.get_path_in_displaycoord()

            if not np.iterable(fillable):
                path = [path]
                fillable = [fillable]

            affine = transforms.IdentityTransform()

            for p, f in zip(path, fillable):
                draw_path(
                    p, affine,
                    self._facecolor if f and self._facecolor[3] else None)
