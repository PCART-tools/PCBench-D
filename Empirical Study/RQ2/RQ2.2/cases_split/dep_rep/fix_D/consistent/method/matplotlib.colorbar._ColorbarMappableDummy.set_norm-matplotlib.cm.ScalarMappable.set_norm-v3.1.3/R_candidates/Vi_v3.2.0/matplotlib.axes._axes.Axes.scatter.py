    @_preprocess_data(replace_names=["x", "y", "s", "linewidths",
                                     "edgecolors", "c", "facecolor",
                                     "facecolors", "color"],
                      label_namer="y")
    @cbook._delete_parameter("3.2", "verts")
    def scatter(self, x, y, s=None, c=None, marker=None, cmap=None, norm=None,
                vmin=None, vmax=None, alpha=None, linewidths=None,
                verts=None, edgecolors=None, *, plotnonfinite=False,
                **kwargs):
        """
        A scatter plot of *y* vs. *x* with varying marker size and/or color.

        Parameters
        ----------
        x, y : scalar or array-like, shape (n, )
            The data positions.

        s : scalar or array-like, shape (n, ), optional
            The marker size in points**2.
            Default is ``rcParams['lines.markersize'] ** 2``.

        c : color, sequence, or sequence of colors, optional
            The marker color. Possible values:

            - A single color format string.
            - A sequence of colors of length n.
            - A scalar or sequence of n numbers to be mapped to colors using
              *cmap* and *norm*.
            - A 2-D array in which the rows are RGB or RGBA.

            Note that *c* should not be a single numeric RGB or RGBA sequence
            because that is indistinguishable from an array of values to be
            colormapped. If you want to specify the same RGB or RGBA value for
            all points, use a 2-D array with a single row.  Otherwise, value-
            matching will have precedence in case of a size matching with *x*
            and *y*.

            Defaults to ``None``. In that case the marker color is determined
            by the value of ``color``, ``facecolor`` or ``facecolors``. In case
            those are not specified or ``None``, the marker color is determined
            by the next color of the ``Axes``' current "shape and fill" color
            cycle. This cycle defaults to :rc:`axes.prop_cycle`.

        marker : `~matplotlib.markers.MarkerStyle`, optional
            The marker style. *marker* can be either an instance of the class
            or the text shorthand for a particular marker.
            Defaults to ``None``, in which case it takes the value of
            :rc:`scatter.marker` = 'o'.
            See `~matplotlib.markers` for more information about marker styles.

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

        linewidths : scalar or array-like, optional, default: None
            The linewidth of the marker edges. Note: The default *edgecolors*
            is 'face'. You may want to change this as well.
            If *None*, defaults to :rc:`lines.linewidth`.

        edgecolors : {'face', 'none', *None*} or color or sequence of color, \
optional.
            The edge color of the marker. Possible values:

            - 'face': The edge color will always be the same as the face color.
            - 'none': No patch boundary will be drawn.
            - A Matplotlib color or sequence of color.

            Defaults to ``None``, in which case it takes the value of
            :rc:`scatter.edgecolors` = 'face'.

            For non-filled markers, the *edgecolors* kwarg is ignored and
            forced to 'face' internally.

        plotnonfinite : boolean, optional, default: False
            Set to plot points with nonfinite *c*, in conjunction with
            `~matplotlib.colors.Colormap.set_bad`.

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
          may be input as N-D arrays, but within scatter they will be
          flattened. The exception is *c*, which will be flattened only if its
          size matches the size of *x* and *y*.

        """
        # Process **kwargs to handle aliases, conflicts with explicit kwargs:

        self._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)
        x = self.convert_xunits(x)
        y = self.convert_yunits(y)

        # np.ma.ravel yields an ndarray, not a masked array,
        # unless its argument is a masked array.
        x = np.ma.ravel(x)
        y = np.ma.ravel(y)
        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        if s is None:
            s = (20 if rcParams['_internal.classic_mode'] else
                 rcParams['lines.markersize'] ** 2.0)
        s = np.ma.ravel(s)
        if len(s) not in (1, x.size):
            raise ValueError("s must be a scalar, or the same size as x and y")

        c, colors, edgecolors = \
            self._parse_scatter_color_args(
                c, edgecolors, kwargs, x.size,
                get_next_color_func=self._get_patches_for_fill.get_next_color)

        if plotnonfinite and colors is None:
            c = np.ma.masked_invalid(c)
            x, y, s, edgecolors, linewidths = \
                cbook._combine_masks(x, y, s, edgecolors, linewidths)
        else:
            x, y, s, c, colors, edgecolors, linewidths = \
                cbook._combine_masks(
                    x, y, s, c, colors, edgecolors, linewidths)

        scales = s   # Renamed for readability below.

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

        offsets = np.ma.column_stack([x, y])

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
            collection.set_array(c)
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
        self._request_autoscale_view()

        return collection
