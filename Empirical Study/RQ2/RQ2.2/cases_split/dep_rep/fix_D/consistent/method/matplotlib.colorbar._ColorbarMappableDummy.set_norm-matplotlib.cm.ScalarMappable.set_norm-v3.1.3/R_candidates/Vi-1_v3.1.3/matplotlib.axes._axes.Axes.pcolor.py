    @_preprocess_data()
    @docstring.dedent_interpd
    def pcolor(self, *args, alpha=None, norm=None, cmap=None, vmin=None,
               vmax=None, **kwargs):
        r"""
        Create a pseudocolor plot with a non-regular rectangular grid.

        Call signature::

            pcolor([X, Y,] C, **kwargs)

        *X* and *Y* can be used to specify the corners of the quadrilaterals.

        .. hint::

            ``pcolor()`` can be very slow for large arrays. In most
            cases you should use the similar but much faster
            `~.Axes.pcolormesh` instead. See there for a discussion of the
            differences.

        Parameters
        ----------
        C : array_like
            A scalar 2-D array. The values will be color-mapped.

        X, Y : array_like, optional
            The coordinates of the quadrilateral corners. The quadrilateral
            for ``C[i,j]`` has corners at::

                (X[i+1, j], Y[i+1, j])          (X[i+1, j+1], Y[i+1, j+1])
                                      +--------+
                                      | C[i,j] |
                                      +--------+
                    (X[i, j], Y[i, j])          (X[i, j+1], Y[i, j+1]),

            Note that the column index corresponds to the
            x-coordinate, and the row index corresponds to y. For
            details, see the :ref:`Notes <axes-pcolor-grid-orientation>`
            section below.

            The dimensions of *X* and *Y* should be one greater than those of
            *C*. Alternatively, *X*, *Y* and *C* may have equal dimensions, in
            which case the last row and column of *C* will be ignored.

            If *X* and/or *Y* are 1-D arrays or column vectors they will be
            expanded as needed into the appropriate 2-D arrays, making a
            rectangular grid.

        cmap : str or `~matplotlib.colors.Colormap`, optional
            A Colormap instance or registered colormap name. The colormap
            maps the *C* values to colors. Defaults to :rc:`image.cmap`.

        norm : `~matplotlib.colors.Normalize`, optional
            The Normalize instance scales the data values to the canonical
            colormap range [0, 1] for mapping to colors. By default, the data
            range is mapped to the colorbar range using linear scaling.

        vmin, vmax : scalar, optional, default: None
            The colorbar range. If *None*, suitable min/max values are
            automatically chosen by the `~.Normalize` instance (defaults to
            the respective min/max values of *C* in case of the default linear
            scaling).

        edgecolors : {'none', None, 'face', color, color sequence}, optional
            The color of the edges. Defaults to 'none'. Possible values:

            - 'none' or '': No edge.
            - *None*: :rc:`patch.edgecolor` will be used. Note that currently
              :rc:`patch.force_edgecolor` has to be True for this to work.
            - 'face': Use the adjacent face color.
            - An mpl color or sequence of colors will set the edge color.

            The singular form *edgecolor* works as an alias.

        alpha : scalar, optional, default: None
            The alpha blending value of the face color, between 0 (transparent)
            and 1 (opaque). Note: The edgecolor is currently not affected by
            this.

        snap : bool, optional, default: False
            Whether to snap the mesh to pixel boundaries.

        Returns
        -------
        collection : `matplotlib.collections.Collection`

        Other Parameters
        ----------------
        antialiaseds : bool, optional, default: False
            The default *antialiaseds* is False if the default
            *edgecolors*\ ="none" is used.  This eliminates artificial lines
            at patch boundaries, and works regardless of the value of alpha.
            If *edgecolors* is not "none", then the default *antialiaseds*
            is taken from :rc:`patch.antialiased`, which defaults to True.
            Stroking the edges may be preferred if *alpha* is 1, but will
            cause artifacts otherwise.

        **kwargs
            Additionally, the following arguments are allowed. They are passed
            along to the `~matplotlib.collections.PolyCollection` constructor:

        %(PolyCollection)s

        See Also
        --------
        pcolormesh : for an explanation of the differences between
            pcolor and pcolormesh.
        imshow : If *X* and *Y* are each equidistant, `~.Axes.imshow` can be a
            faster alternative.

        Notes
        -----

        **Masked arrays**

        *X*, *Y* and *C* may be masked arrays. If either ``C[i, j]``, or one
        of the vertices surrounding ``C[i,j]`` (*X* or *Y* at
        ``[i, j], [i+1, j], [i, j+1], [i+1, j+1]``) is masked, nothing is
        plotted.

        .. _axes-pcolor-grid-orientation:

        **Grid orientation**

        The grid orientation follows the standard matrix convention: An array
        *C* with shape (nrows, ncolumns) is plotted with the column number as
        *X* and the row number as *Y*.

        **Handling of pcolor() end-cases**

        ``pcolor()`` displays all columns of *C* if *X* and *Y* are not
        specified, or if *X* and *Y* have one more column than *C*.
        If *X* and *Y* have the same number of columns as *C* then the last
        column of *C* is dropped. Similarly for the rows.

        Note: This behavior is different from MATLAB's ``pcolor()``, which
        always discards the last row and column of *C*.
        """
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

        unmask = ~mask
        X1 = ma.filled(X[:-1, :-1])[unmask]
        Y1 = ma.filled(Y[:-1, :-1])[unmask]
        X2 = ma.filled(X[1:, :-1])[unmask]
        Y2 = ma.filled(Y[1:, :-1])[unmask]
        X3 = ma.filled(X[1:, 1:])[unmask]
        Y3 = ma.filled(Y[1:, 1:])[unmask]
        X4 = ma.filled(X[:-1, 1:])[unmask]
        Y4 = ma.filled(Y[:-1, 1:])[unmask]
        npoly = len(X1)

        xy = np.stack([X1, Y1, X2, Y2, X3, Y3, X4, Y4, X1, Y1], axis=-1)
        verts = xy.reshape((npoly, 5, 2))

        C = ma.filled(C[:Ny - 1, :Nx - 1])[unmask]

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
        if 'antialiaseds' not in kwargs and cbook._str_lower_equal(ec, "none"):
            kwargs['antialiaseds'] = False

        kwargs.setdefault('snap', False)

        collection = mcoll.PolyCollection(verts, **kwargs)

        collection.set_alpha(alpha)
        collection.set_array(C)
        if norm is not None and not isinstance(norm, mcolors.Normalize):
            raise ValueError(
                "'norm' must be an instance of 'mcolors.Normalize'")
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
