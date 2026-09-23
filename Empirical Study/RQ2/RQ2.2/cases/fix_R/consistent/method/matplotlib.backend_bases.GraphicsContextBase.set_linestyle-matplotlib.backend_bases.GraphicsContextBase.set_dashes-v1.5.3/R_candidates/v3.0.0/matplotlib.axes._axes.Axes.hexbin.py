    @_preprocess_data(replace_names=["x", "y"], label_namer="y")
    @docstring.dedent_interpd
    def hexbin(self, x, y, C=None, gridsize=100, bins=None,
               xscale='linear', yscale='linear', extent=None,
               cmap=None, norm=None, vmin=None, vmax=None,
               alpha=None, linewidths=None, edgecolors='face',
               reduce_C_function=np.mean, mincnt=None, marginals=False,
               **kwargs):
        """
        Make a hexagonal binning plot.

        Make a hexagonal binning plot of *x* versus *y*, where *x*,
        *y* are 1-D sequences of the same length, *N*. If *C* is *None*
        (the default), this is a histogram of the number of occurrences
        of the observations at (x[i],y[i]).

        If *C* is specified, it specifies values at the coordinate
        (x[i], y[i]). These values are accumulated for each hexagonal
        bin and then reduced according to *reduce_C_function*, which
        defaults to `numpy.mean`. (If *C* is specified, it must also
        be a 1-D sequence of the same length as *x* and *y*.)

        Parameters
        ----------
        x, y : array or masked array

        C : array or masked array, optional, default is *None*

        gridsize : int or (int, int), optional, default is 100
            The number of hexagons in the *x*-direction, default is
            100. The corresponding number of hexagons in the
            *y*-direction is chosen such that the hexagons are
            approximately regular. Alternatively, gridsize can be a
            tuple with two elements specifying the number of hexagons
            in the *x*-direction and the *y*-direction.

        bins : 'log' or int or sequence, optional, default is *None*
            If *None*, no binning is applied; the color of each hexagon
            directly corresponds to its count value.

            If 'log', use a logarithmic scale for the color
            map. Internally, :math:`log_{10}(i+1)` is used to
            determine the hexagon color.

            If an integer, divide the counts in the specified number
            of bins, and color the hexagons accordingly.

            If a sequence of values, the values of the lower bound of
            the bins to be used.

        xscale : {'linear', 'log'}, optional, default is 'linear'
            Use a linear or log10 scale on the horizontal axis.

        yscale : {'linear', 'log'}, optional, default is 'linear'
            Use a linear or log10 scale on the vertical axis.

        mincnt : int > 0, optional, default is *None*
            If not *None*, only display cells with more than *mincnt*
            number of points in the cell

        marginals : bool, optional, default is *False*
            if marginals is *True*, plot the marginal density as
            colormapped rectagles along the bottom of the x-axis and
            left of the y-axis

        extent : scalar, optional, default is *None*
            The limits of the bins. The default assigns the limits
            based on *gridsize*, *x*, *y*, *xscale* and *yscale*.

            If *xscale* or *yscale* is set to 'log', the limits are
            expected to be the exponent for a power of 10. E.g. for
            x-limits of 1 and 50 in 'linear' scale and y-limits
            of 10 and 1000 in 'log' scale, enter (1, 50, 1, 3).

            Order of scalars is (left, right, bottom, top).

        Other Parameters
        ----------------
        cmap : object, optional, default is *None*
            a :class:`matplotlib.colors.Colormap` instance. If *None*,
            defaults to rc ``image.cmap``.

        norm : object, optional, default is *None*
            :class:`matplotlib.colors.Normalize` instance is used to
            scale luminance data to 0,1.

        vmin, vmax : scalar, optional, default is *None*
            *vmin* and *vmax* are used in conjunction with *norm* to
            normalize luminance data. If *None*, the min and max of the
            color array *C* are used.  Note if you pass a norm instance
            your settings for *vmin* and *vmax* will be ignored.

        alpha : scalar between 0 and 1, optional, default is *None*
            the alpha value for the patches

        linewidths : scalar, optional, default is *None*
            If *None*, defaults to 1.0.

        edgecolors : {'face', 'none', *None*} or color, optional

            If 'face' (the default), draws the edges in the same color as the
            fill color.

            If 'none', no edge is drawn; this can sometimes lead to unsightly
            unpainted pixels between the hexagons.

            If *None*, draws outlines in the default color.

            If a matplotlib color arg, draws outlines in the specified color.

        Returns
        -------
        polycollection
            A `.PolyCollection` instance; use `.PolyCollection.get_array` on
            this to get the counts in each hexagon.

            If *marginals* is *True*, horizontal
            bar and vertical bar (both PolyCollections) will be attached
            to the return collection as attributes *hbar* and *vbar*.

        Notes
        -----
        The standard descriptions of all the
        :class:`~matplotlib.collections.Collection` parameters:

            %(Collection)s

        """
        self._process_unit_info(xdata=x, ydata=y, kwargs=kwargs)

        x, y, C = cbook.delete_masked_points(x, y, C)

        # Set the size of the hexagon grid
        if iterable(gridsize):
            nx, ny = gridsize
        else:
            nx = gridsize
            ny = int(nx / math.sqrt(3))
        # Count the number of data in each hexagon
        x = np.array(x, float)
        y = np.array(y, float)
        if xscale == 'log':
            if np.any(x <= 0.0):
                raise ValueError("x contains non-positive values, so can not"
                                 " be log-scaled")
            x = np.log10(x)
        if yscale == 'log':
            if np.any(y <= 0.0):
                raise ValueError("y contains non-positive values, so can not"
                                 " be log-scaled")
            y = np.log10(y)
        if extent is not None:
            xmin, xmax, ymin, ymax = extent
        else:
            xmin, xmax = (np.min(x), np.max(x)) if len(x) else (0, 1)
            ymin, ymax = (np.min(y), np.max(y)) if len(y) else (0, 1)

            # to avoid issues with singular data, expand the min/max pairs
            xmin, xmax = mtransforms.nonsingular(xmin, xmax, expander=0.1)
            ymin, ymax = mtransforms.nonsingular(ymin, ymax, expander=0.1)

        # In the x-direction, the hexagons exactly cover the region from
        # xmin to xmax. Need some padding to avoid roundoff errors.
        padding = 1.e-9 * (xmax - xmin)
        xmin -= padding
        xmax += padding
        sx = (xmax - xmin) / nx
        sy = (ymax - ymin) / ny

        if marginals:
            xorig = x.copy()
            yorig = y.copy()

        x = (x - xmin) / sx
        y = (y - ymin) / sy
        ix1 = np.round(x).astype(int)
        iy1 = np.round(y).astype(int)
        ix2 = np.floor(x).astype(int)
        iy2 = np.floor(y).astype(int)

        nx1 = nx + 1
        ny1 = ny + 1
        nx2 = nx
        ny2 = ny
        n = nx1 * ny1 + nx2 * ny2

        d1 = (x - ix1) ** 2 + 3.0 * (y - iy1) ** 2
        d2 = (x - ix2 - 0.5) ** 2 + 3.0 * (y - iy2 - 0.5) ** 2
        bdist = (d1 < d2)
        if C is None:
            lattice1 = np.zeros((nx1, ny1))
            lattice2 = np.zeros((nx2, ny2))

            cond1 = (0 <= ix1) * (ix1 < nx1) * (0 <= iy1) * (iy1 < ny1)
            cond2 = (0 <= ix2) * (ix2 < nx2) * (0 <= iy2) * (iy2 < ny2)

            cond1 *= bdist
            cond2 *= np.logical_not(bdist)
            ix1, iy1 = ix1[cond1], iy1[cond1]
            ix2, iy2 = ix2[cond2], iy2[cond2]

            for ix, iy in zip(ix1, iy1):
                lattice1[ix, iy] += 1
            for ix, iy in zip(ix2, iy2):
                lattice2[ix, iy] += 1

            # threshold
            if mincnt is not None:
                lattice1[lattice1 < mincnt] = np.nan
                lattice2[lattice2 < mincnt] = np.nan
            accum = np.hstack((lattice1.ravel(),
                               lattice2.ravel()))
            good_idxs = ~np.isnan(accum)

        else:
            if mincnt is None:
                mincnt = 0

            # create accumulation arrays
            lattice1 = np.empty((nx1, ny1), dtype=object)
            for i in range(nx1):
                for j in range(ny1):
                    lattice1[i, j] = []
            lattice2 = np.empty((nx2, ny2), dtype=object)
            for i in range(nx2):
                for j in range(ny2):
                    lattice2[i, j] = []

            for i in range(len(x)):
                if bdist[i]:
                    if 0 <= ix1[i] < nx1 and 0 <= iy1[i] < ny1:
                        lattice1[ix1[i], iy1[i]].append(C[i])
                else:
                    if 0 <= ix2[i] < nx2 and 0 <= iy2[i] < ny2:
                        lattice2[ix2[i], iy2[i]].append(C[i])

            for i in range(nx1):
                for j in range(ny1):
                    vals = lattice1[i, j]
                    if len(vals) > mincnt:
                        lattice1[i, j] = reduce_C_function(vals)
                    else:
                        lattice1[i, j] = np.nan
            for i in range(nx2):
                for j in range(ny2):
                    vals = lattice2[i, j]
                    if len(vals) > mincnt:
                        lattice2[i, j] = reduce_C_function(vals)
                    else:
                        lattice2[i, j] = np.nan

            accum = np.hstack((lattice1.astype(float).ravel(),
                               lattice2.astype(float).ravel()))
            good_idxs = ~np.isnan(accum)

        offsets = np.zeros((n, 2), float)
        offsets[:nx1 * ny1, 0] = np.repeat(np.arange(nx1), ny1)
        offsets[:nx1 * ny1, 1] = np.tile(np.arange(ny1), nx1)
        offsets[nx1 * ny1:, 0] = np.repeat(np.arange(nx2) + 0.5, ny2)
        offsets[nx1 * ny1:, 1] = np.tile(np.arange(ny2), nx2) + 0.5
        offsets[:, 0] *= sx
        offsets[:, 1] *= sy
        offsets[:, 0] += xmin
        offsets[:, 1] += ymin
        # remove accumulation bins with no data
        offsets = offsets[good_idxs, :]
        accum = accum[good_idxs]

        polygon = np.zeros((6, 2), float)
        polygon[:, 0] = sx * np.array([0.5, 0.5, 0.0, -0.5, -0.5, 0.0])
        polygon[:, 1] = sy * np.array([-0.5, 0.5, 1.0, 0.5, -0.5, -1.0]) / 3.0

        if linewidths is None:
            linewidths = [1.0]

        if xscale == 'log' or yscale == 'log':
            polygons = np.expand_dims(polygon, 0) + np.expand_dims(offsets, 1)
            if xscale == 'log':
                polygons[:, :, 0] = 10.0 ** polygons[:, :, 0]
                xmin = 10.0 ** xmin
                xmax = 10.0 ** xmax
                self.set_xscale(xscale)
            if yscale == 'log':
                polygons[:, :, 1] = 10.0 ** polygons[:, :, 1]
                ymin = 10.0 ** ymin
                ymax = 10.0 ** ymax
                self.set_yscale(yscale)
            collection = mcoll.PolyCollection(
                polygons,
                edgecolors=edgecolors,
                linewidths=linewidths,
                )
        else:
            collection = mcoll.PolyCollection(
                [polygon],
                edgecolors=edgecolors,
                linewidths=linewidths,
                offsets=offsets,
                transOffset=mtransforms.IdentityTransform(),
                offset_position="data"
                )

        # Check for valid norm
        if norm is not None and not isinstance(norm, mcolors.Normalize):
            msg = "'norm' must be an instance of 'mcolors.Normalize'"
            raise ValueError(msg)

        # Set normalizer if bins is 'log'
        if bins == 'log':
            if norm is not None:
                warnings.warn("Only one of 'bins' and 'norm' arguments can be "
                              "supplied, ignoring bins={}".format(bins))
            else:
                norm = mcolors.LogNorm()
            bins = None

        if isinstance(norm, mcolors.LogNorm):
            if (accum == 0).any():
                # make sure we have no zeros
                accum += 1

        # autoscale the norm with curren accum values if it hasn't
        # been set
        if norm is not None:
            if norm.vmin is None and norm.vmax is None:
                norm.autoscale(accum)

        if bins is not None:
            if not iterable(bins):
                minimum, maximum = min(accum), max(accum)
                bins -= 1  # one less edge than bins
                bins = minimum + (maximum - minimum) * np.arange(bins) / bins
            bins = np.sort(bins)
            accum = bins.searchsorted(accum)

        collection.set_array(accum)
        collection.set_cmap(cmap)
        collection.set_norm(norm)
        collection.set_alpha(alpha)
        collection.update(kwargs)

        if vmin is not None or vmax is not None:
            collection.set_clim(vmin, vmax)
        else:
            collection.autoscale_None()

        corners = ((xmin, ymin), (xmax, ymax))
        self.update_datalim(corners)
        collection.sticky_edges.x[:] = [xmin, xmax]
        collection.sticky_edges.y[:] = [ymin, ymax]
        self.autoscale_view(tight=True)

        # add the collection last
        self.add_collection(collection, autolim=False)
        if not marginals:
            return collection

        if C is None:
            C = np.ones(len(x))

        def coarse_bin(x, y, coarse):
            ind = coarse.searchsorted(x).clip(0, len(coarse) - 1)
            mus = np.zeros(len(coarse))
            for i in range(len(coarse)):
                yi = y[ind == i]
                if len(yi) > 0:
                    mu = reduce_C_function(yi)
                else:
                    mu = np.nan
                mus[i] = mu
            return mus

        coarse = np.linspace(xmin, xmax, gridsize)

        xcoarse = coarse_bin(xorig, C, coarse)
        valid = ~np.isnan(xcoarse)
        verts, values = [], []
        for i, val in enumerate(xcoarse):
            thismin = coarse[i]
            if i < len(coarse) - 1:
                thismax = coarse[i + 1]
            else:
                thismax = thismin + np.diff(coarse)[-1]

            if not valid[i]:
                continue

            verts.append([(thismin, 0),
                          (thismin, 0.05),
                          (thismax, 0.05),
                          (thismax, 0)])
            values.append(val)

        values = np.array(values)
        trans = self.get_xaxis_transform(which='grid')

        hbar = mcoll.PolyCollection(verts, transform=trans, edgecolors='face')

        hbar.set_array(values)
        hbar.set_cmap(cmap)
        hbar.set_norm(norm)
        hbar.set_alpha(alpha)
        hbar.update(kwargs)
        self.add_collection(hbar, autolim=False)

        coarse = np.linspace(ymin, ymax, gridsize)
        ycoarse = coarse_bin(yorig, C, coarse)
        valid = ~np.isnan(ycoarse)
        verts, values = [], []
        for i, val in enumerate(ycoarse):
            thismin = coarse[i]
            if i < len(coarse) - 1:
                thismax = coarse[i + 1]
            else:
                thismax = thismin + np.diff(coarse)[-1]
            if not valid[i]:
                continue
            verts.append([(0, thismin), (0.0, thismax),
                          (0.05, thismax), (0.05, thismin)])
            values.append(val)

        values = np.array(values)

        trans = self.get_yaxis_transform(which='grid')

        vbar = mcoll.PolyCollection(verts, transform=trans, edgecolors='face')
        vbar.set_array(values)
        vbar.set_cmap(cmap)
        vbar.set_norm(norm)
        vbar.set_alpha(alpha)
        vbar.update(kwargs)
        self.add_collection(vbar, autolim=False)

        collection.hbar = hbar
        collection.vbar = vbar

        def on_changed(collection):
            hbar.set_cmap(collection.get_cmap())
            hbar.set_clim(collection.get_clim())
            vbar.set_cmap(collection.get_cmap())
            vbar.set_clim(collection.get_clim())

        collection.callbacksSM.connect('changed', on_changed)

        return collection
