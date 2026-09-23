    @_preprocess_data(replace_names=["x", "y", "s", "linewidths",
                                     "edgecolors", "c", "facecolor",
                                     "facecolors", "color"],
                      label_namer="y")
    def scatter(self, x, y, s=None, c=None, marker=None, cmap=None, norm=None,
                vmin=None, vmax=None, alpha=None, linewidths=None,
                verts=None, edgecolors=None,
                **kwargs):
        """
        A scatter plot of *y* vs *x* with varying marker size and/or color.

        Parameters
        ----------
        x, y : array_like, shape (n, )
            The data positions.

        s : scalar or array_like, shape (n, ), optional
            The marker size in points**2.
            Default is ``rcParams['lines.markersize'] ** 2``.

        c : color, sequence, or sequence of color, optional, default: 'b'
            The marker color. Possible values:

            - A single color format string.
            - A sequence of color specifications of length n.
            - A sequence of n numbers to be mapped to colors using *cmap* and
              *norm*.
            - A 2-D array in which the rows are RGB or RGBA.

            Note that *c* should not be a single numeric RGB or RGBA sequence
            because that is indistinguishable from an array of values to be
            colormapped. If you want to specify the same RGB or RGBA value for
            all points, use a 2-D array with a single row.  Otherwise, value-
            matching will have precedence in case of a size matching with *x*
            and *y*.

        marker : `~matplotlib.markers.MarkerStyle`, optional, default: 'o'
            The marker style. *marker* can be either an instance of the class
            or the text shorthand for a particular marker.
            See `~matplotlib.markers` for more information marker styles.

        cmap : `~matplotlib.colors.Colormap`, optional, default: None
            A `.Colormap` instance or registered colormap name. *cmap* is only
            used if *c* is an array of floats. If ``None``, defaults to rc
            ``image.cmap``.

        norm : `~matplotlib.colors.Normalize`, optional, default: None
            A `.Normalize` instance is used to scale luminance data to 0, 1.
            *norm* is only used if *c* is an array of floats. If *None*, use
            the default `.colors.Normalize`.

        vmin, vmax : scalar, optional, default: None
            *vmin* and *vmax* are used in conjunction with *norm* to normalize
            luminance data. If None, the respective min and max of the color
            array is used. *vmin* and *vmax* are ignored if you pass a *norm*
            instance.

        alpha : scalar, optional, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        linewidths : scalar or array_like, optional, default: None
            The linewidth of the marker edges. Note: The default *edgecolors*
            is 'face'. You may want to change this as well.
            If *None*, defaults to rcParams ``lines.linewidth``.

        edgecolors : color or sequence of color, optional, default: 'face'
            The edge color of the marker. Possible values:

            - 'face': The edge color will always be the same as the face color.
            - 'none': No patch boundary will be drawn.
            - A matplotib color.

            For non-filled markers, the *edgecolors* kwarg is ignored and
            forced to 'face' internally.

        Returns
        -------
        paths : `~matplotlib.collections.PathCollection`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.collections.Collection` properties

        See Also
        --------
        plot : To plot scatter plots when markers are identical in size and
            color.

        Notes
        -----

        * The `.plot` function will be faster for scatterplots where markers
          don't vary in size or color.

        * Any or all of *x*, *y*, *s*, and *c* may be masked arrays, in which
          case all masks will be combined and only unmasked points will be
          plotted.

        * Fundamentally, scatter works with 1-D arrays; *x*, *y*, *s*, and *c*
          may be input as 2-D arrays, but within scatter they will be
          flattened. The exception is *c*, which will be flattened only if its
          size matches the size of *x* and *y*.

        """
        # Process **kwargs to handle aliases, conflicts with explicit kwargs:
        facecolors = None
        edgecolors = kwargs.pop('edgecolor', edgecolors)
        fc = kwargs.pop('facecolors', None)
        fc = kwargs.pop('facecolor', fc)
        if fc is not None:
            facecolors = fc
        co = kwargs.pop('color', None)
        if co is not None:
            try:
                mcolors.to_rgba_array(co)
            except ValueError:
                raise ValueError("'color' kwarg must be an mpl color"
                                 " spec or sequence of color specs.\n"
                                 "For a sequence of values to be color-mapped,"
                                 " use the 'c' argument instead.")
            if edgecolors is None:
                edgecolors = co
            if facecolors is None:
                facecolors = co
            if c is not None:
                raise ValueError("Supply a 'c' argument or a 'color'"
                                 " kwarg but not both; they differ but"
                                 " their functionalities overlap.")
        if c is None:
            if facecolors is not None:
                c = facecolors
            else:
                if rcParams['_internal.classic_mode']:
                    c = 'b'  # The original default
                else:
                    c = self._get_patches_for_fill.get_next_color()
            c_none = True
        else:
            c_none = False

        if edgecolors is None and not rcParams['_internal.classic_mode']:
            edgecolors = 'face'

        self._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)
        x = self.convert_xunits(x)
        y = self.convert_yunits(y)

        # np.ma.ravel yields an ndarray, not a masked array,
        # unless its argument is a masked array.
        xy_shape = (np.shape(x), np.shape(y))
        x = np.ma.ravel(x)
        y = np.ma.ravel(y)
        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        if s is None:
            if rcParams['_internal.classic_mode']:
                s = 20
            else:
                s = rcParams['lines.markersize'] ** 2.0

        s = np.ma.ravel(s)  # This doesn't have to match x, y in size.

        # After this block, c_array will be None unless
        # c is an array for mapping.  The potential ambiguity
        # with a sequence of 3 or 4 numbers is resolved in
        # favor of mapping, not rgb or rgba.

        # Convenience vars to track shape mismatch *and* conversion failures.
        valid_shape = True  # will be put to the test!
        n_elem = -1  # used only for (some) exceptions

        if c_none or co is not None:
            c_array = None
        else:
            try:  # First, does 'c' look suitable for value-mapping?
                c_array = np.asanyarray(c, dtype=float)
                n_elem = c_array.shape[0]
                if c_array.shape in xy_shape:
                    c = np.ma.ravel(c_array)
                else:
                    if c_array.shape in ((3,), (4,)):
                        _log.warning(
                            "'c' argument looks like a single numeric RGB or "
                            "RGBA sequence, which should be avoided as value-"
                            "mapping will have precedence in case its length "
                            "matches with 'x' & 'y'.  Please use a 2-D array "
                            "with a single row if you really want to specify "
                            "the same RGB or RGBA value for all points.")
                    # Wrong size; it must not be intended for mapping.
                    valid_shape = False
                    c_array = None
            except ValueError:
                # Failed to make a floating-point array; c must be color specs.
                c_array = None

        if c_array is None:
            try:  # Then is 'c' acceptable as PathCollection facecolors?
                colors = mcolors.to_rgba_array(c)
                n_elem = colors.shape[0]
                if colors.shape[0] not in (0, 1, x.size, y.size):
                    # NB: remember that a single color is also acceptable.
                    # Besides *colors* will be an empty array if c == 'none'.
                    valid_shape = False
                    raise ValueError
            except ValueError:
                if not valid_shape:  # but at least one conversion succeeded.
                    raise ValueError(
                        "'c' argument has {nc} elements, which is not "
                        "acceptable for use with 'x' with size {xs}, "
                        "'y' with size {ys}."
                        .format(nc=n_elem, xs=x.size, ys=y.size)
                    )
                # Both the mapping *and* the RGBA conversion failed: pretty
                # severe failure => one may appreciate a verbose feedback.
                raise ValueError(
                    "'c' argument must either be valid as mpl color(s) "
                    "or as numbers to be mapped to colors. "
                    "Here c = {}."  # <- beware, could be long depending on c.
                    .format(c)
                )
        else:
            colors = None  # use cmap, norm after collection is created

        # `delete_masked_points` only modifies arguments of the same length as
        # `x`.
        x, y, s, c, colors, edgecolors, linewidths =\
            cbook.delete_masked_points(
                x, y, s, c, colors, edgecolors, linewidths)

        scales = s   # Renamed for readability below.

        # to be API compatible
        if verts is not None:
            cbook.warn_deprecated("3.0", name="'verts'", obj_type="kwarg",
                                  alternative="'marker'")
            if marker is None:
                marker = verts

        # load default marker from rcParams
        if marker is None:
            marker = rcParams['scatter.marker']

        if isinstance(marker, mmarkers.MarkerStyle):
            marker_obj = marker
        else:
            marker_obj = mmarkers.MarkerStyle(marker)

        path = marker_obj.get_path().transformed(
            marker_obj.get_transform())
        if not marker_obj.is_filled():
            edgecolors = 'face'
            linewidths = rcParams['lines.linewidth']

        offsets = np.column_stack([x, y])

        collection = mcoll.PathCollection(
                (path,), scales,
                facecolors=colors,
                edgecolors=edgecolors,
                linewidths=linewidths,
                offsets=offsets,
                transOffset=kwargs.pop('transform', self.transData),
                alpha=alpha
                )
        collection.set_transform(mtransforms.IdentityTransform())
        collection.update(kwargs)

        if colors is None:
            if norm is not None and not isinstance(norm, mcolors.Normalize):
                raise ValueError(
                    "'norm' must be an instance of 'mcolors.Normalize'")
            collection.set_array(np.asarray(c))
            collection.set_cmap(cmap)
            collection.set_norm(norm)

            if vmin is not None or vmax is not None:
                collection.set_clim(vmin, vmax)
            else:
                collection.autoscale_None()

        # Classic mode only:
        # ensure there are margins to allow for the
        # finite size of the symbols.  In v2.x, margins
        # are present by default, so we disable this
        # scatter-specific override.
        if rcParams['_internal.classic_mode']:
            if self._xmargin < 0.05 and x.size > 0:
                self.set_xmargin(0.05)
            if self._ymargin < 0.05 and x.size > 0:
                self.set_ymargin(0.05)

        self.add_collection(collection)
        self.autoscale_view()

        return collection
