    @_preprocess_data(label_namer=None)
    @docstring.dedent_interpd
    def pcolormesh(self, *args, **kwargs):
        """
        Plot a quadrilateral mesh.

        Call signatures::

          pcolormesh(C)
          pcolormesh(X, Y, C)
          pcolormesh(C, **kwargs)

        Create a pseudocolor plot of a 2-D array.

        pcolormesh is similar to :func:`~matplotlib.pyplot.pcolor`,
        but uses a different mechanism and returns a different
        object; pcolor returns a
        :class:`~matplotlib.collections.PolyCollection` but pcolormesh
        returns a
        :class:`~matplotlib.collections.QuadMesh`.  It is much faster,
        so it is almost always preferred for large arrays.

        *C* may be a masked array, but *X* and *Y* may not.  Masked
        array support is implemented via *cmap* and *norm*; in
        contrast, :func:`~matplotlib.pyplot.pcolor` simply does not
        draw quadrilaterals with masked colors or vertices.

        Keyword arguments:

          *cmap*: [ *None* | Colormap ]
            A :class:`matplotlib.colors.Colormap` instance. If *None*, use
            rc settings.

          *norm*: [ *None* | Normalize ]
            A :class:`matplotlib.colors.Normalize` instance is used to
            scale luminance data to 0,1. If *None*, defaults to
            :func:`normalize`.

          *vmin*/*vmax*: [ *None* | scalar ]
            *vmin* and *vmax* are used in conjunction with *norm* to
            normalize luminance data.  If either is *None*, it
            is autoscaled to the respective min or max
            of the color array *C*.  If not *None*, *vmin* or
            *vmax* passed in here override any pre-existing values
            supplied in the *norm* instance.

          *shading*: [ 'flat' | 'gouraud' ]
            'flat' indicates a solid color for each quad.  When
            'gouraud', each quad will be Gouraud shaded.  When gouraud
            shading, edgecolors is ignored.

          *edgecolors*: [*None* | ``'None'`` | ``'face'`` | color |
                         color sequence]

            If *None*, the rc setting is used by default.

            If ``'None'``, edges will not be visible.

            If ``'face'``, edges will have the same color as the faces.

            An mpl color or sequence of colors will set the edge color

          *alpha*: ``0 <= scalar <= 1``  or *None*
            the alpha blending value

        Return value is a :class:`matplotlib.collections.QuadMesh`
        object.

        kwargs can be used to control the
        :class:`matplotlib.collections.QuadMesh` properties:

        %(QuadMesh)s

        .. seealso::

            :func:`~matplotlib.pyplot.pcolor`
                For an explanation of the grid orientation
                (:ref:`Grid Orientation <axes-pcolor-grid-orientation>`)
                and the expansion of 1-D *X* and/or *Y* to 2-D arrays.
        """
        if not self._hold:
            self.cla()

        alpha = kwargs.pop('alpha', None)
        norm = kwargs.pop('norm', None)
        cmap = kwargs.pop('cmap', None)
        vmin = kwargs.pop('vmin', None)
        vmax = kwargs.pop('vmax', None)
        shading = kwargs.pop('shading', 'flat').lower()
        antialiased = kwargs.pop('antialiased', False)
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
            msg = "'norm' must be an instance of 'mcolors.Normalize'"
            raise ValueError(msg)
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
