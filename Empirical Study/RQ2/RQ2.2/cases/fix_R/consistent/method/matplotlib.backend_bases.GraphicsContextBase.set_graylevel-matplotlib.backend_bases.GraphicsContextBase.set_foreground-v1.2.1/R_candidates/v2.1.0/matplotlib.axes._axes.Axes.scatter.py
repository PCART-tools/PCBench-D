    @_preprocess_data(replace_names=["x", "y", "s", "linewidths",
                                     "edgecolors", "c", "facecolor",
                                     "facecolors", "color"],
                      label_namer="y")
    def scatter(self, x, y, s=None, c=None, marker=None, cmap=None, norm=None,
                vmin=None, vmax=None, alpha=None, linewidths=None,
                verts=None, edgecolors=None,
                **kwargs):
        """
        Make a scatter plot of `x` vs `y`.

        Marker size is scaled by `s` and marker color is mapped to `c`.

        Parameters
        ----------
        x, y : array_like, shape (n, )
            Input data

        s : scalar or array_like, shape (n, ), optional
            size in points^2.  Default is `rcParams['lines.markersize'] ** 2`.

        c : color, sequence, or sequence of color, optional, default: 'b'
            `c` can be a single color format string, or a sequence of color
            specifications of length `N`, or a sequence of `N` numbers to be
            mapped to colors using the `cmap` and `norm` specified via kwargs
            (see below). Note that `c` should not be a single numeric RGB or
            RGBA sequence because that is indistinguishable from an array of
            values to be colormapped.  `c` can be a 2-D array in which the
            rows are RGB or RGBA, however, including the case of a single
            row to specify the same color for all points.

        marker : `~matplotlib.markers.MarkerStyle`, optional, default: 'o'
            See `~matplotlib.markers` for more information on the different
            styles of markers scatter supports. `marker` can be either
            an instance of the class or the text shorthand for a particular
            marker.

        cmap : `~matplotlib.colors.Colormap`, optional, default: None
            A `~matplotlib.colors.Colormap` instance or registered name.
            `cmap` is only used if `c` is an array of floats. If None,
            defaults to rc `image.cmap`.

        norm : `~matplotlib.colors.Normalize`, optional, default: None
            A `~matplotlib.colors.Normalize` instance is used to scale
            luminance data to 0, 1. `norm` is only used if `c` is an array of
            floats. If `None`, use the default :func:`normalize`.

        vmin, vmax : scalar, optional, default: None
            `vmin` and `vmax` are used in conjunction with `norm` to normalize
            luminance data.  If either are `None`, the min and max of the
            color array is used.  Note if you pass a `norm` instance, your
            settings for `vmin` and `vmax` will be ignored.

        alpha : scalar, optional, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque)

        linewidths : scalar or array_like, optional, default: None
            If None, defaults to (lines.linewidth,).

        verts : sequence of (x, y), optional
            If `marker` is None, these vertices will be used to
            construct the marker.  The center of the marker is located
            at (0,0) in normalized units.  The overall marker is rescaled
            by ``s``.

        edgecolors : color or sequence of color, optional, default: None
            If None, defaults to 'face'

            If 'face', the edge color will always be the same as
            the face color.

            If it is 'none', the patch boundary will not
            be drawn.

            For non-filled markers, the `edgecolors` kwarg
            is ignored and forced to 'face' internally.

        Returns
        -------
        paths : `~matplotlib.collections.PathCollection`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.collections.Collection` properties

        See Also
        --------
        plot : to plot scatter plots when markers are identical in size and
            color

        Notes
        -----

        * The `plot` function will be faster for scatterplots where markers
          don't vary in size or color.

        * Any or all of `x`, `y`, `s`, and `c` may be masked arrays, in which
          case all masks will be combined and only unmasked points will be
          plotted.

          Fundamentally, scatter works with 1-D arrays; `x`, `y`, `s`, and `c`
          may be input as 2-D arrays, but within scatter they will be
          flattened. The exception is `c`, which will be flattened only if its
          size matches the size of `x` and `y`.

        """

        if not self._hold:
            self.cla()

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
                                 "For a sequence of values to be"
                                 " color-mapped, use the 'c' kwarg instead.")
            if edgecolors is None:
                edgecolors = co
            if facecolors is None:
                facecolors = co
            if c is not None:
                raise ValueError("Supply a 'c' kwarg or a 'color' kwarg"
                                 " but not both; they differ but"
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
        if c_none or co is not None:
            c_array = None
        else:
            try:
                c_array = np.asanyarray(c, dtype=float)
                if c_array.shape in xy_shape:
                    c = np.ma.ravel(c_array)
                else:
                    # Wrong size; it must not be intended for mapping.
                    c_array = None
            except ValueError:
                # Failed to make a floating-point array; c must be color specs.
                c_array = None

        if c_array is None:
            try:
                # must be acceptable as PathCollection facecolors
                colors = mcolors.to_rgba_array(c)
            except ValueError:
                # c not acceptable as PathCollection facecolor
                msg = ("c of shape {0} not acceptable as a color sequence "
                       "for x with size {1}, y with size {2}")
                raise ValueError(msg.format(c.shape, x.size, y.size))
        else:
            colors = None  # use cmap, norm after collection is created

        # `delete_masked_points` only modifies arguments of the same length as
        # `x`.
        x, y, s, c, colors, edgecolors, linewidths =\
            cbook.delete_masked_points(
                x, y, s, c, colors, edgecolors, linewidths)

        scales = s   # Renamed for readability below.

        # to be API compatible
        if marker is None and verts is not None:
            marker = (verts, 0)
            verts = None

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
                msg = "'norm' must be an instance of 'mcolors.Normalize'"
                raise ValueError(msg)
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
