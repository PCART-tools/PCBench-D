@docstring.dedent_interpd
class QuadContourSet(ContourSet):
    """
    Create and store a set of contour lines or filled regions.

    This class is typically not instantiated directly by the user but by
    `~.Axes.contour` and `~.Axes.contourf`.

    %(contour_set_attributes)s
    """

    def _process_args(self, *args, corner_mask=None, **kwargs):
        """
        Process args and kwargs.
        """
        if isinstance(args[0], QuadContourSet):
            if self.levels is None:
                self.levels = args[0].levels
            self.zmin = args[0].zmin
            self.zmax = args[0].zmax
            self._corner_mask = args[0]._corner_mask
            contour_generator = args[0]._contour_generator
            self._mins = args[0]._mins
            self._maxs = args[0]._maxs
        else:
            import matplotlib._contour as _contour

            if corner_mask is None:
                corner_mask = mpl.rcParams['contour.corner_mask']
            self._corner_mask = corner_mask

            x, y, z = self._contour_args(args, kwargs)

            _mask = ma.getmask(z)
            if _mask is ma.nomask or not _mask.any():
                _mask = None

            contour_generator = _contour.QuadContourGenerator(
                x, y, z.filled(), _mask, self._corner_mask, self.nchunk)

            t = self.get_transform()

            # if the transform is not trans data, and some part of it
            # contains transData, transform the xs and ys to data coordinates
            if (t != self.axes.transData and
                    any(t.contains_branch_seperately(self.axes.transData))):
                trans_to_data = t - self.axes.transData
                pts = np.vstack([x.flat, y.flat]).T
                transformed_pts = trans_to_data.transform(pts)
                x = transformed_pts[..., 0]
                y = transformed_pts[..., 1]

            self._mins = [ma.min(x), ma.min(y)]
            self._maxs = [ma.max(x), ma.max(y)]

        self._contour_generator = contour_generator

        return kwargs

    def _get_allsegs_and_allkinds(self):
        """Compute ``allsegs`` and ``allkinds`` using C extension."""
        allsegs = []
        if self.filled:
            lowers, uppers = self._get_lowers_and_uppers()
            allkinds = []
            for level, level_upper in zip(lowers, uppers):
                vertices, kinds = \
                    self._contour_generator.create_filled_contour(
                        level, level_upper)
                allsegs.append(vertices)
                allkinds.append(kinds)
        else:
            allkinds = None
            for level in self.levels:
                vertices = self._contour_generator.create_contour(level)
                allsegs.append(vertices)
        return allsegs, allkinds

    def _contour_args(self, args, kwargs):
        if self.filled:
            fn = 'contourf'
        else:
            fn = 'contour'
        Nargs = len(args)
        if Nargs <= 2:
            z = ma.asarray(args[0], dtype=np.float64)
            x, y = self._initialize_x_y(z)
            args = args[1:]
        elif Nargs <= 4:
            x, y, z = self._check_xyz(args[:3], kwargs)
            args = args[3:]
        else:
            raise TypeError("Too many arguments to %s; see help(%s)" %
                            (fn, fn))
        z = ma.masked_invalid(z, copy=False)
        self.zmax = float(z.max())
        self.zmin = float(z.min())
        if self.logscale and self.zmin <= 0:
            z = ma.masked_where(z <= 0, z)
            _api.warn_external('Log scale: values of z <= 0 have been masked')
            self.zmin = float(z.min())
        self._process_contour_level_args(args)
        return (x, y, z)

    def _check_xyz(self, args, kwargs):
        """
        Check that the shapes of the input arrays match; if x and y are 1D,
        convert them to 2D using meshgrid.
        """
        x, y = args[:2]
        x, y = self.axes._process_unit_info([("x", x), ("y", y)], kwargs)

        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        z = ma.asarray(args[2], dtype=np.float64)

        if z.ndim != 2:
            raise TypeError(f"Input z must be 2D, not {z.ndim}D")
        if z.shape[0] < 2 or z.shape[1] < 2:
            raise TypeError(f"Input z must be at least a (2, 2) shaped array, "
                            f"but has shape {z.shape}")
        Ny, Nx = z.shape

        if x.ndim != y.ndim:
            raise TypeError(f"Number of dimensions of x ({x.ndim}) and y "
                            f"({y.ndim}) do not match")
        if x.ndim == 1:
            nx, = x.shape
            ny, = y.shape
            if nx != Nx:
                raise TypeError(f"Length of x ({nx}) must match number of "
                                f"columns in z ({Nx})")
            if ny != Ny:
                raise TypeError(f"Length of y ({ny}) must match number of "
                                f"rows in z ({Ny})")
            x, y = np.meshgrid(x, y)
        elif x.ndim == 2:
            if x.shape != z.shape:
                raise TypeError(
                    f"Shapes of x {x.shape} and z {z.shape} do not match")
            if y.shape != z.shape:
                raise TypeError(
                    f"Shapes of y {y.shape} and z {z.shape} do not match")
        else:
            raise TypeError(f"Inputs x and y must be 1D or 2D, not {x.ndim}D")

        return x, y, z

    def _initialize_x_y(self, z):
        """
        Return X, Y arrays such that contour(Z) will match imshow(Z)
        if origin is not None.
        The center of pixel Z[i, j] depends on origin:
        if origin is None, x = j, y = i;
        if origin is 'lower', x = j + 0.5, y = i + 0.5;
        if origin is 'upper', x = j + 0.5, y = Nrows - i - 0.5
        If extent is not None, x and y will be scaled to match,
        as in imshow.
        If origin is None and extent is not None, then extent
        will give the minimum and maximum values of x and y.
        """
        if z.ndim != 2:
            raise TypeError(f"Input z must be 2D, not {z.ndim}D")
        elif z.shape[0] < 2 or z.shape[1] < 2:
            raise TypeError(f"Input z must be at least a (2, 2) shaped array, "
                            f"but has shape {z.shape}")
        else:
            Ny, Nx = z.shape
        if self.origin is None:  # Not for image-matching.
            if self.extent is None:
                return np.meshgrid(np.arange(Nx), np.arange(Ny))
            else:
                x0, x1, y0, y1 = self.extent
                x = np.linspace(x0, x1, Nx)
                y = np.linspace(y0, y1, Ny)
                return np.meshgrid(x, y)
        # Match image behavior:
        if self.extent is None:
            x0, x1, y0, y1 = (0, Nx, 0, Ny)
        else:
            x0, x1, y0, y1 = self.extent
        dx = (x1 - x0) / Nx
        dy = (y1 - y0) / Ny
        x = x0 + (np.arange(Nx) + 0.5) * dx
        y = y0 + (np.arange(Ny) + 0.5) * dy
        if self.origin == 'upper':
            y = y[::-1]
        return np.meshgrid(x, y)

    _contour_doc = """
        `.contour` and `.contourf` draw contour lines and filled contours,
        respectively.  Except as noted, function signatures and return values
        are the same for both versions.

        Parameters
        ----------
        X, Y : array-like, optional
            The coordinates of the values in *Z*.

            *X* and *Y* must both be 2D with the same shape as *Z* (e.g.
            created via `numpy.meshgrid`), or they must both be 1-D such
            that ``len(X) == M`` is the number of columns in *Z* and
            ``len(Y) == N`` is the number of rows in *Z*.

            If not given, they are assumed to be integer indices, i.e.
            ``X = range(M)``, ``Y = range(N)``.

        Z : (M, N) array-like
            The height values over which the contour is drawn.

        levels : int or array-like, optional
            Determines the number and positions of the contour lines / regions.

            If an int *n*, use `~matplotlib.ticker.MaxNLocator`, which tries
            to automatically choose no more than *n+1* "nice" contour levels
            between *vmin* and *vmax*.

            If array-like, draw contour lines at the specified levels.
            The values must be in increasing order.

        Returns
        -------
        `~.contour.QuadContourSet`

        Other Parameters
        ----------------
        corner_mask : bool, default: :rc:`contour.corner_mask`
            Enable/disable corner masking, which only has an effect if *Z* is
            a masked array.  If ``False``, any quad touching a masked point is
            masked out.  If ``True``, only the triangular corners of quads
            nearest those points are always masked out, other triangular
            corners comprising three unmasked points are contoured as usual.

        colors : color string or sequence of colors, optional
            The colors of the levels, i.e. the lines for `.contour` and the
            areas for `.contourf`.

            The sequence is cycled for the levels in ascending order. If the
            sequence is shorter than the number of levels, it's repeated.

            As a shortcut, single color strings may be used in place of
            one-element lists, i.e. ``'red'`` instead of ``['red']`` to color
            all levels with the same color. This shortcut does only work for
            color strings, not for other ways of specifying colors.

            By default (value *None*), the colormap specified by *cmap*
            will be used.

        alpha : float, default: 1
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        cmap : str or `.Colormap`, default: :rc:`image.cmap`
            A `.Colormap` instance or registered colormap name. The colormap
            maps the level values to colors.

            If both *colors* and *cmap* are given, an error is raised.

        norm : `~matplotlib.colors.Normalize`, optional
            If a colormap is used, the `.Normalize` instance scales the level
            values to the canonical colormap range [0, 1] for mapping to
            colors. If not given, the default linear scaling is used.

        vmin, vmax : float, optional
            If not *None*, either or both of these values will be supplied to
            the `.Normalize` instance, overriding the default color scaling
            based on *levels*.

        origin : {*None*, 'upper', 'lower', 'image'}, default: None
            Determines the orientation and exact position of *Z* by specifying
            the position of ``Z[0, 0]``.  This is only relevant, if *X*, *Y*
            are not given.

            - *None*: ``Z[0, 0]`` is at X=0, Y=0 in the lower left corner.
            - 'lower': ``Z[0, 0]`` is at X=0.5, Y=0.5 in the lower left corner.
            - 'upper': ``Z[0, 0]`` is at X=N+0.5, Y=0.5 in the upper left
              corner.
            - 'image': Use the value from :rc:`image.origin`.

        extent : (x0, x1, y0, y1), optional
            If *origin* is not *None*, then *extent* is interpreted as in
            `.imshow`: it gives the outer pixel boundaries. In this case, the
            position of Z[0, 0] is the center of the pixel, not a corner. If
            *origin* is *None*, then (*x0*, *y0*) is the position of Z[0, 0],
            and (*x1*, *y1*) is the position of Z[-1, -1].

            This argument is ignored if *X* and *Y* are specified in the call
            to contour.

        locator : ticker.Locator subclass, optional
            The locator is used to determine the contour levels if they
            are not given explicitly via *levels*.
            Defaults to `~.ticker.MaxNLocator`.

        extend : {'neither', 'both', 'min', 'max'}, default: 'neither'
            Determines the ``contourf``-coloring of values that are outside the
            *levels* range.

            If 'neither', values outside the *levels* range are not colored.
            If 'min', 'max' or 'both', color the values below, above or below
            and above the *levels* range.

            Values below ``min(levels)`` and above ``max(levels)`` are mapped
            to the under/over values of the `.Colormap`. Note that most
            colormaps do not have dedicated colors for these by default, so
            that the over and under values are the edge values of the colormap.
            You may want to set these values explicitly using
            `.Colormap.set_under` and `.Colormap.set_over`.

            .. note::

                An existing `.QuadContourSet` does not get notified if
                properties of its colormap are changed. Therefore, an explicit
                call `.QuadContourSet.changed()` is needed after modifying the
                colormap. The explicit call can be left out, if a colorbar is
                assigned to the `.QuadContourSet` because it internally calls
                `.QuadContourSet.changed()`.

            Example::

                x = np.arange(1, 10)
                y = x.reshape(-1, 1)
                h = x * y

                cs = plt.contourf(h, levels=[10, 30, 50],
                    colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
                cs.cmap.set_over('red')
                cs.cmap.set_under('blue')
                cs.changed()

        xunits, yunits : registered units, optional
            Override axis units by specifying an instance of a
            :class:`matplotlib.units.ConversionInterface`.

        antialiased : bool, optional
            Enable antialiasing, overriding the defaults.  For
            filled contours, the default is *True*.  For line contours,
            it is taken from :rc:`lines.antialiased`.

        nchunk : int >= 0, optional
            If 0, no subdivision of the domain.  Specify a positive integer to
            divide the domain into subdomains of *nchunk* by *nchunk* quads.
            Chunking reduces the maximum length of polygons generated by the
            contouring algorithm which reduces the rendering workload passed
            on to the backend and also requires slightly less RAM.  It can
            however introduce rendering artifacts at chunk boundaries depending
            on the backend, the *antialiased* flag and value of *alpha*.

        linewidths : float or array-like, default: :rc:`contour.linewidth`
            *Only applies to* `.contour`.

            The line width of the contour lines.

            If a number, all levels will be plotted with this linewidth.

            If a sequence, the levels in ascending order will be plotted with
            the linewidths in the order specified.

            If None, this falls back to :rc:`lines.linewidth`.

        linestyles : {*None*, 'solid', 'dashed', 'dashdot', 'dotted'}, optional
            *Only applies to* `.contour`.

            If *linestyles* is *None*, the default is 'solid' unless the lines
            are monochrome.  In that case, negative contours will take their
            linestyle from :rc:`contour.negative_linestyle` setting.

            *linestyles* can also be an iterable of the above strings
            specifying a set of linestyles to be used. If this
            iterable is shorter than the number of contour levels
            it will be repeated as necessary.

        hatches : list[str], optional
            *Only applies to* `.contourf`.

            A list of cross hatch patterns to use on the filled areas.
            If None, no hatching will be added to the contour.
            Hatching is supported in the PostScript, PDF, SVG and Agg
            backends only.

        Notes
        -----
        1. `.contourf` differs from the MATLAB version in that it does not draw
           the polygon edges. To draw edges, add line contours with calls to
           `.contour`.

        2. `.contourf` fills intervals that are closed at the top; that is, for
           boundaries *z1* and *z2*, the filled region is::

              z1 < Z <= z2

           except for the lowest interval, which is closed on both sides (i.e.
           it includes the lowest value).
        """
