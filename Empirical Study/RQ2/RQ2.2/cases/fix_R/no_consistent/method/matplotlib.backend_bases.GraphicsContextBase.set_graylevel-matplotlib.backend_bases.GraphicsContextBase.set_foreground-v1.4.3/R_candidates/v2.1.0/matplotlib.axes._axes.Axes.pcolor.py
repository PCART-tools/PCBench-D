    @_preprocess_data(label_namer=None)
    @docstring.dedent_interpd
    def pcolor(self, *args, **kwargs):
        """
        Create a pseudocolor plot of a 2-D array.

        Call signatures::

            pcolor(C, **kwargs)
            pcolor(X, Y, C, **kwargs)

        pcolor can be very slow for large arrays; consider
        using the similar but much faster
        :func:`~matplotlib.pyplot.pcolormesh` instead.

        Parameters
        ----------
        C : array_like
            An array of color values.

        X, Y : array_like, optional
            If given, specify the (x, y) coordinates of the colored
            quadrilaterals; the quadrilateral for ``C[i,j]`` has corners at::

                (X[i,   j],   Y[i,   j]),
                (X[i,   j+1], Y[i,   j+1]),
                (X[i+1, j],   Y[i+1, j]),
                (X[i+1, j+1], Y[i+1, j+1])

            Ideally the dimensions of ``X`` and ``Y`` should be one greater
            than those of ``C``; if the dimensions are the same, then the last
            row and column of ``C`` will be ignored.

            Note that the column index corresponds to the
            x-coordinate, and the row index corresponds to y; for
            details, see the :ref:`Grid Orientation
            <axes-pcolor-grid-orientation>` section below.

            If either or both of ``X`` and ``Y`` are 1-D arrays or column
            vectors, they will be expanded as needed into the appropriate 2-D
            arrays, making a rectangular grid.

        cmap : `~matplotlib.colors.Colormap`, optional, default: None
            If `None`, default to rc settings.

        norm : `matplotlib.colors.Normalize`, optional, default: None
            An instance is used to scale luminance data to (0, 1).
            If `None`, defaults to :func:`normalize`.

        vmin, vmax : scalar, optional, default: None
            ``vmin`` and ``vmax`` are used in conjunction with ``norm`` to
            normalize luminance data.  If either is `None`, it is autoscaled to
            the respective min or max of the color array ``C``.  If not `None`,
            ``vmin`` or ``vmax`` passed in here override any pre-existing
            values supplied in the ``norm`` instance.

        edgecolors : {None, 'none', color, color sequence}
            If None, the rc setting is used by default.
            If 'none', edges will not be visible.
            An mpl color or sequence of colors will set the edge color.

        alpha : scalar, optional, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        snap : bool, optional, default: False
            Whether to snap the mesh to pixel boundaries.

        Returns
        -------
        collection : `matplotlib.collections.Collection`

        Other Parameters
        ----------------
        antialiaseds : bool, optional, default: False
            The default ``antialiaseds`` is False if the default
            ``edgecolors="none"`` is used.  This eliminates artificial lines
            at patch boundaries, and works regardless of the value of alpha.
            If ``edgecolors`` is not "none", then the default ``antialiaseds``
            is taken from ``rcParams['patch.antialiased']``, which defaults to
            True. Stroking the edges may be preferred if ``alpha`` is 1, but
            will cause artifacts otherwise.

        **kwargs :

            Any unused keyword arguments are passed along to the
            `~matplotlib.collections.PolyCollection` constructor:

        %(PolyCollection)s

        See Also
        --------
        pcolormesh : for an explanation of the differences between
            pcolor and pcolormesh.

        Notes
        -----
        .. _axes-pcolor-grid-orientation:

        ``X``, ``Y`` and ``C`` may be masked arrays. If either C[i, j], or one
        of the vertices surrounding C[i,j] (``X`` or ``Y`` at [i, j], [i+1, j],
        [i, j+1], [i+1, j+1]) is masked, nothing is plotted.

        The grid orientation follows the MATLAB convention: an array ``C`` with
        shape (nrows, ncolumns) is plotted with the column number as ``X`` and
        the row number as ``Y``, increasing up; hence it is plotted the way the
        array would be printed, except that the ``Y`` axis is reversed. That
        is, ``C`` is taken as ``C`` (y, x).

        Similarly for :func:`meshgrid`::

            x = np.arange(5)
            y = np.arange(3)
            X, Y = np.meshgrid(x, y)

        is equivalent to::

            X = array([[0, 1, 2, 3, 4],
                       [0, 1, 2, 3, 4],
                       [0, 1, 2, 3, 4]])

            Y = array([[0, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1],
                       [2, 2, 2, 2, 2]])

        so if you have::

            C = rand(len(x), len(y))

        then you need to transpose C::

            pcolor(X, Y, C.T)

        or::

            pcolor(C.T)

        MATLAB :func:`pcolor` always discards the last row and column of ``C``,
        but Matplotlib displays the last row and column if ``X`` and ``Y`` are
        not specified, or if ``X`` and ``Y`` have one more row and column than
        ``C``.
        """

        if not self._hold:
            self.cla()

        alpha = kwargs.pop('alpha', None)
        norm = kwargs.pop('norm', None)
        cmap = kwargs.pop('cmap', None)
        vmin = kwargs.pop('vmin', None)
        vmax = kwargs.pop('vmax', None)

        X, Y, C = self._pcolorargs('pcolor', *args, allmatch=False)
        Ny, Nx = X.shape

        # unit conversion allows e.g. datetime objects as axis values
        self._process_unit_info(xdata=X, ydata=Y, kwargs=kwargs)
        X = self.convert_xunits(X)
        Y = self.convert_yunits(Y)

        # convert to MA, if necessary.
        C = ma.asarray(C)
        X = ma.asarray(X)
        Y = ma.asarray(Y)

        mask = ma.getmaskarray(X) + ma.getmaskarray(Y)
        xymask = (mask[0:-1, 0:-1] + mask[1:, 1:] +
                  mask[0:-1, 1:] + mask[1:, 0:-1])
        # don't plot if C or any of the surrounding vertices are masked.
        mask = ma.getmaskarray(C) + xymask

        newaxis = np.newaxis
        compress = np.compress

        ravelmask = (mask == 0).ravel()
        X1 = compress(ravelmask, ma.filled(X[0:-1, 0:-1]).ravel())
        Y1 = compress(ravelmask, ma.filled(Y[0:-1, 0:-1]).ravel())
        X2 = compress(ravelmask, ma.filled(X[1:, 0:-1]).ravel())
        Y2 = compress(ravelmask, ma.filled(Y[1:, 0:-1]).ravel())
        X3 = compress(ravelmask, ma.filled(X[1:, 1:]).ravel())
        Y3 = compress(ravelmask, ma.filled(Y[1:, 1:]).ravel())
        X4 = compress(ravelmask, ma.filled(X[0:-1, 1:]).ravel())
        Y4 = compress(ravelmask, ma.filled(Y[0:-1, 1:]).ravel())
        npoly = len(X1)

        xy = np.concatenate((X1[:, newaxis], Y1[:, newaxis],
                             X2[:, newaxis], Y2[:, newaxis],
                             X3[:, newaxis], Y3[:, newaxis],
                             X4[:, newaxis], Y4[:, newaxis],
                             X1[:, newaxis], Y1[:, newaxis]),
                            axis=1)
        verts = xy.reshape((npoly, 5, 2))

        C = compress(ravelmask, ma.filled(C[0:Ny - 1, 0:Nx - 1]).ravel())

        linewidths = (0.25,)
        if 'linewidth' in kwargs:
            kwargs['linewidths'] = kwargs.pop('linewidth')
        kwargs.setdefault('linewidths', linewidths)

        if 'edgecolor' in kwargs:
            kwargs['edgecolors'] = kwargs.pop('edgecolor')
        ec = kwargs.setdefault('edgecolors', 'none')

        # aa setting will default via collections to patch.antialiased
        # unless the boundary is not stroked, in which case the
        # default will be False; with unstroked boundaries, aa
        # makes artifacts that are often disturbing.
        if 'antialiased' in kwargs:
            kwargs['antialiaseds'] = kwargs.pop('antialiased')
        if 'antialiaseds' not in kwargs and (
                isinstance(ec, six.string_types) and ec.lower() == "none"):
            kwargs['antialiaseds'] = False

        kwargs.setdefault('snap', False)

        collection = mcoll.PolyCollection(verts, **kwargs)

        collection.set_alpha(alpha)
        collection.set_array(C)
        if norm is not None and not isinstance(norm, mcolors.Normalize):
            msg = "'norm' must be an instance of 'mcolors.Normalize'"
            raise ValueError(msg)
        collection.set_cmap(cmap)
        collection.set_norm(norm)
        collection.set_clim(vmin, vmax)
        collection.autoscale_None()
        self.grid(False)

        x = X.compressed()
        y = Y.compressed()

        # Transform from native to data coordinates?
        t = collection._transform
        if (not isinstance(t, mtransforms.Transform) and
            hasattr(t, '_as_mpl_transform')):
            t = t._as_mpl_transform(self.axes)

        if t and any(t.contains_branch_seperately(self.transData)):
            trans_to_data = t - self.transData
            pts = np.vstack([x, y]).T.astype(float)
            transformed_pts = trans_to_data.transform(pts)
            x = transformed_pts[..., 0]
            y = transformed_pts[..., 1]

        self.add_collection(collection, autolim=False)

        minx = np.min(x)
        maxx = np.max(x)
        miny = np.min(y)
        maxy = np.max(y)
        collection.sticky_edges.x[:] = [minx, maxx]
        collection.sticky_edges.y[:] = [miny, maxy]
        corners = (minx, miny), (maxx, maxy)
        self.update_datalim(corners)
        self.autoscale_view()
        return collection
