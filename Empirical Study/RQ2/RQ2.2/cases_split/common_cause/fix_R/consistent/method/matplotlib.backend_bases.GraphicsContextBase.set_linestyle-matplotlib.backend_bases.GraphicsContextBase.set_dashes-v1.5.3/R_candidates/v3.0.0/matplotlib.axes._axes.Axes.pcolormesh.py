    @_preprocess_data(label_namer=None)
    @docstring.dedent_interpd
    def pcolormesh(self, *args, alpha=None, norm=None, cmap=None, vmin=None,
                   vmax=None, shading='flat', antialiased=False, **kwargs):
        """
        Create a pseudocolor plot with a non-regular rectangular grid.

        Call signature::

            pcolor([X, Y,] C, **kwargs)

        *X* and *Y* can be used to specify the corners of the quadrilaterals.

        .. note::

           ``pcolormesh()`` is similar to :func:`~Axes.pcolor`. It's much
           faster and preferred in most cases. For a detailed discussion on
           the differences see
           :ref:`Differences between pcolor() and pcolormesh()
           <differences-pcolor-pcolormesh>`.

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
            details, see the :ref:`Notes <axes-pcolormesh-grid-orientation>`
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
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        shading : {'flat', 'gouraud'}, optional
            The fill style, Possible values:

            - 'flat': A solid color is used for each quad. The color of the
              quad (i, j), (i+1, j), (i, j+1), (i+1, j+1) is given by
              ``C[i,j]``.
            - 'gouraud': Each quad will be Gouraud shaded: The color of the
              corners (i', j') are given by ``C[i',j']``. The color values of
              the area in between is interpolated from the corner values.
              When Gouraud shading is used, *edgecolors* is ignored.

        snap : bool, optional, default: False
            Whether to snap the mesh to pixel boundaries.

        Returns
        -------
        mesh : `matplotlib.collections.QuadMesh`

        Other Parameters
        ----------------
        **kwargs
            Additionally, the following arguments are allowed. They are passed
            along to the `~matplotlib.collections.QuadMesh` constructor:

        %(QuadMesh)s


        See Also
        --------
        pcolor : An alternative implementation with slightly different
            features. For a detailed discussion on the differences see
            :ref:`Differences between pcolor() and pcolormesh()
            <differences-pcolor-pcolormesh>`.
        imshow : If *X* and *Y* are each equidistant, `~.Axes.imshow` can be a
            faster alternative.

        Notes
        -----

        **Masked arrays**

        *C* may be a masked array. If ``C[i, j]`` is masked, the corresponding
        quadrilateral will be transparent. Masking of *X* and *Y* is not
        supported. Use `~.Axes.pcolor` if you need this functionality.

        .. _axes-pcolormesh-grid-orientation:

        **Grid orientation**

        The grid orientation follows the standard matrix convention: An array
        *C* with shape (nrows, ncolumns) is plotted with the column number as
        *X* and the row number as *Y*.

        .. _differences-pcolor-pcolormesh:

        **Differences between pcolor() and pcolormesh()**

        Both methods are used to create a pseudocolor plot of a 2-D array
        using quadrilaterals.

        The main difference lies in the created object and internal data
        handling:
        While `~.Axes.pcolor` returns a `.PolyCollection`, `~.Axes.pcolormesh`
        returns a `.QuadMesh`. The latter is more specialized for the given
        purpose and thus is faster. It should almost always be preferred.

        There is also a slight difference in the handling of masked arrays.
        Both `~.Axes.pcolor` and `~.Axes.pcolormesh` support masked arrays
        for *C*. However, only `~.Axes.pcolor` supports masked arrays for *X*
        and *Y*. The reason lies in the internal handling of the masked values.
        `~.Axes.pcolor` leaves out the respective polygons from the
        PolyCollection. `~.Axes.pcolormesh` sets the facecolor of the masked
        elements to transparent. You can see the difference when using
        edgecolors. While all edges are drawn irrespective of masking in a
        QuadMesh, the edge between two adjacent masked quadrilaterals in
        `~.Axes.pcolor` is not drawn as the corresponding polygons do not
        exist in the PolyCollection.

        Another difference is the support of Gouraud shading in
        `~.Axes.pcolormesh`, which is not available with `~.Axes.pcolor`.

        """
        shading = shading.lower()
        kwargs.setdefault('edgecolors', 'None')

        allmatch = (shading == 'gouraud')

        X, Y, C = self._pcolorargs('pcolormesh', *args, allmatch=allmatch)
        Ny, Nx = X.shape
        X = X.ravel()
        Y = Y.ravel()
        # unit conversion allows e.g. datetime objects as axis values
        self._process_unit_info(xdata=X, ydata=Y, kwargs=kwargs)
        X = self.convert_xunits(X)
        Y = self.convert_yunits(Y)

        # convert to one dimensional arrays
        C = C.ravel()
        coords = np.column_stack((X, Y)).astype(float, copy=False)
        collection = mcoll.QuadMesh(Nx - 1, Ny - 1, coords,
                                    antialiased=antialiased, shading=shading,
                                    **kwargs)
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

        # Transform from native to data coordinates?
        t = collection._transform
        if (not isinstance(t, mtransforms.Transform) and
            hasattr(t, '_as_mpl_transform')):
            t = t._as_mpl_transform(self.axes)

        if t and any(t.contains_branch_seperately(self.transData)):
            trans_to_data = t - self.transData
            coords = trans_to_data.transform(coords)

        self.add_collection(collection, autolim=False)

        minx, miny = np.min(coords, axis=0)
        maxx, maxy = np.max(coords, axis=0)
        collection.sticky_edges.x[:] = [minx, maxx]
        collection.sticky_edges.y[:] = [miny, maxy]
        corners = (minx, miny), (maxx, maxy)
        self.update_datalim(corners)
        self.autoscale_view()
        return collection
