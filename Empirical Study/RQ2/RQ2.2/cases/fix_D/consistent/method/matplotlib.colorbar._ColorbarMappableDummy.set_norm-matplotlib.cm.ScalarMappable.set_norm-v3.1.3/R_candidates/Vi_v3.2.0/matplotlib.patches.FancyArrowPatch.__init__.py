    @docstring.dedent_interpd
    def __init__(self, posA=None, posB=None,
                 path=None,
                 arrowstyle="simple",
                 arrow_transmuter=None,
                 connectionstyle="arc3",
                 connector=None,
                 patchA=None,
                 patchB=None,
                 shrinkA=2,
                 shrinkB=2,
                 mutation_scale=1,
                 mutation_aspect=None,
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
        posA, posB : (float, float), optional (default: None)
            (x, y) coordinates of arrow tail and arrow head respectively.

        path : `~matplotlib.path.Path`, optional (default: None)
            If provided, an arrow is drawn along this path and *patchA*,
            *patchB*, *shrinkA*, and *shrinkB* are ignored.

        arrowstyle : str or `.ArrowStyle`, optional (default: 'simple')
            Describes how the fancy arrow will be
            drawn. It can be string of the available arrowstyle names,
            with optional comma-separated attributes, or an
            :class:`ArrowStyle` instance. The optional attributes are meant to
            be scaled with the *mutation_scale*. The following arrow styles are
            available:

            %(AvailableArrowstyles)s

        arrow_transmuter
            Ignored.

        connectionstyle : str or `.ConnectionStyle` or None, optional \
(default: 'arc3')
            Describes how *posA* and *posB* are connected. It can be an
            instance of the :class:`ConnectionStyle` class or a string of the
            connectionstyle name, with optional comma-separated attributes. The
            following connection styles are available:

            %(AvailableConnectorstyles)s

        connector
            Ignored.

        patchA, patchB : `.Patch`, optional (default: None)
            Head and tail patch respectively. :class:`matplotlib.patch.Patch`
            instance.

        shrinkA, shrinkB : float, optional (default: 2)
            Shrinking factor of the tail and head of the arrow respectively.

        mutation_scale : float, optional (default: 1)
            Value with which attributes of *arrowstyle* (e.g., *head_length*)
            will be scaled.

        mutation_aspect : None or float, optional (default: None)
            The height of the rectangle will be squeezed by this value before
            the mutation and the mutated box will be stretched by the inverse
            of it.

        dpi_cor : float, optional (default: 1)
            dpi_cor is currently used for linewidth-related things and shrink
            factor. Mutation scale is affected by this.

        Other Parameters
        ----------------
        **kwargs : `.Patch` properties, optional
            Here is a list of available `.Patch` properties:

        %(Patch)s

            In contrast to other patches, the default ``capstyle`` and
            ``joinstyle`` for `FancyArrowPatch` are set to ``"round"``.
        """
        if arrow_transmuter is not None:
            cbook.warn_deprecated(
                3.0,
                message=('The "arrow_transmuter" keyword argument is not used,'
                         ' and will be removed in Matplotlib 3.1'),
                name='arrow_transmuter',
                obj_type='keyword argument')
        if connector is not None:
            cbook.warn_deprecated(
                3.0,
                message=('The "connector" keyword argument is not used,'
                         ' and will be removed in Matplotlib 3.1'),
                name='connector',
                obj_type='keyword argument')
        # Traditionally, the cap- and joinstyle for FancyArrowPatch are round
        kwargs.setdefault("joinstyle", "round")
        kwargs.setdefault("capstyle", "round")

        Patch.__init__(self, **kwargs)

        if posA is not None and posB is not None and path is None:
            self._posA_posB = [posA, posB]

            if connectionstyle is None:
                connectionstyle = "arc3"
            self.set_connectionstyle(connectionstyle)

        elif posA is None and posB is None and path is not None:
            self._posA_posB = None
        else:
            raise ValueError("either posA and posB, or path need to provided")

        self.patchA = patchA
        self.patchB = patchB
        self.shrinkA = shrinkA
        self.shrinkB = shrinkB

        self._path_original = path

        self.set_arrowstyle(arrowstyle)

        self._mutation_scale = mutation_scale
        self._mutation_aspect = mutation_aspect

        self.set_dpi_cor(dpi_cor)
