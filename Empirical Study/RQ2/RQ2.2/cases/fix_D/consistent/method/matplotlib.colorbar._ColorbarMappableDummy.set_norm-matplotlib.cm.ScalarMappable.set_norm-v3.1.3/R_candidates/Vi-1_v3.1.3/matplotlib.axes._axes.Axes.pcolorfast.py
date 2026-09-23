    @_preprocess_data()
    @docstring.dedent_interpd
    def pcolorfast(self, *args, alpha=None, norm=None, cmap=None, vmin=None,
                   vmax=None, **kwargs):
        """
        Create a pseudocolor plot with a non-regular rectangular grid.

        Call signature::

          ax.pcolorfast([X, Y], C, /, **kwargs)

        This method is similar to ~.Axes.pcolor` and `~.Axes.pcolormesh`.
        It's designed to provide the fastest pcolor-type plotting with the
        Agg backend. To achieve this, it uses different algorithms internally
        depending on the complexity of the input grid (regular rectangular,
        non-regular rectangular or arbitrary quadrilateral).

        .. warning::

           This method is experimental. Compared to `~.Axes.pcolor` or
           `~.Axes.pcolormesh` it has some limitations:

           - It supports only flat shading (no outlines)
           - It lacks support for log scaling of the axes.
           - It does not have a have a pyplot wrapper.

        Parameters
        ----------
        C : array-like(M, N)
            A 2D array or masked array. The values will be color-mapped.
            This argument can only be passed positionally.

            C can in some cases be 3D with the last dimension as rgb(a).
            This is available when C qualifies for image or pcolorimage type,
            will throw a TypeError if C is 3D and quadmesh.

        X, Y : tuple or array-like, default: ``(0, N)``, ``(0, M)``
            *X* and *Y* are used to specify the coordinates of the
            quadrilaterals. There are different ways to do this:

            - Use tuples ``X=(xmin, xmax)`` and ``Y=(ymin, ymax)`` to define
              a *uniform rectangular grid*.

              The tuples define the outer edges of the grid. All individual
              quadrilaterals will be of the same size. This is the fastest
              version.

            - Use 1D arrays *X*, *Y* to specify a *non-uniform rectangular
              grid*.

              In this case *X* and *Y* have to be monotonic 1D arrays of length
              *N+1* and *M+1*, specifying the x and y boundaries of the cells.

              The speed is intermediate. Note: The grid is checked, and if
              found to be uniform the fast version is used.

            - Use 2D arrays *X*, *Y* if you need an *arbitrary quadrilateral
              grid* (i.e. if the quadrilaterals are not rectangular).

              In this case *X* and *Y* are 2D arrays with shape (M, N),
              specifying the x and y coordinates of the corners of the colored
              quadrilaterals. See `~.Axes.pcolormesh` for details.

              This is the most general, but the slowest to render.  It may
              produce faster and more compact output using ps, pdf, and
              svg backends, however.

            These arguments can only be passed positionally.

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

        alpha : scalar, optional, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        snap : bool, optional, default: False
            Whether to snap the mesh to pixel boundaries.

        Returns
        -------
        image : `.AxesImage` or `.PcolorImage` or `.QuadMesh`
            The return type depends on the type of grid:

            - `.AxesImage` for a regular rectangular grid.
            - `.PcolorImage` for a non-regular rectangular grid.
            - `.QuadMesh` for a non-rectangular grid.

        Notes
        -----
        .. [notes section required to get data note injection right]

        """
        if norm is not None and not isinstance(norm, mcolors.Normalize):
            raise ValueError(
                "'norm' must be an instance of 'mcolors.Normalize'")

        C = args[-1]
        nr, nc = np.shape(C)[:2]
        if len(args) == 1:
            style = "image"
            x = [0, nc]
            y = [0, nr]
        elif len(args) == 3:
            x, y = args[:2]
            x = np.asarray(x)
            y = np.asarray(y)
            if x.ndim == 1 and y.ndim == 1:
                if x.size == 2 and y.size == 2:
                    style = "image"
                else:
                    dx = np.diff(x)
                    dy = np.diff(y)
                    if (np.ptp(dx) < 0.01 * np.abs(dx.mean()) and
                        np.ptp(dy) < 0.01 * np.abs(dy.mean())):
                        style = "image"
                    else:
                        style = "pcolorimage"
            elif x.ndim == 2 and y.ndim == 2:
                if C.ndim > 2:
                    raise ValueError(
                        'pcolorfast needs to use quadmesh, '
                        'which is not supported when x and y are 2D and C 3D')
                style = "quadmesh"
            else:
                raise TypeError("arguments do not match valid signatures")
        else:
            raise TypeError("need 1 argument or 3 arguments")

        if style == "quadmesh":

            # convert to one dimensional arrays
            # This should also be moved to the QuadMesh class

            # data point in each cell is value at lower left corner
            C = ma.ravel(C)
            X = x.ravel()
            Y = y.ravel()
            Nx = nc + 1
            Ny = nr + 1

            # The following needs to be cleaned up; the renderer
            # requires separate contiguous arrays for X and Y,
            # but the QuadMesh class requires the 2D array.
            coords = np.empty(((Nx * Ny), 2), np.float64)
            coords[:, 0] = X
            coords[:, 1] = Y

            # The QuadMesh class can also be changed to
            # handle relevant superclass kwargs; the initializer
            # should do much more than it does now.
            collection = mcoll.QuadMesh(nc, nr, coords, 0, edgecolors="None")
            collection.set_alpha(alpha)
            collection.set_array(C)
            collection.set_cmap(cmap)
            collection.set_norm(norm)
            self.add_collection(collection, autolim=False)
            xl, xr, yb, yt = X.min(), X.max(), Y.min(), Y.max()
            ret = collection

        else:  # It's one of the two image styles.
            xl, xr, yb, yt = x[0], x[-1], y[0], y[-1]

            if style == "image":
                im = mimage.AxesImage(self, cmap, norm,
                                      interpolation='nearest',
                                      origin='lower',
                                      extent=(xl, xr, yb, yt),
                                      **kwargs)
                im.set_data(C)
                im.set_alpha(alpha)
            elif style == "pcolorimage":
                im = mimage.PcolorImage(self, x, y, C,
                                        cmap=cmap,
                                        norm=norm,
                                        alpha=alpha,
                                        **kwargs)
                im.set_extent((xl, xr, yb, yt))
            self.add_image(im)
            ret = im

        if vmin is not None or vmax is not None:
            ret.set_clim(vmin, vmax)
        else:
            ret.autoscale_None()
        if ret.get_clip_path() is None:
            # image does not already have clipping set, clip to axes patch
            ret.set_clip_path(self.patch)

        ret.sticky_edges.x[:] = [xl, xr]
        ret.sticky_edges.y[:] = [yb, yt]
        self.update_datalim(np.array([[xl, yb], [xr, yt]]))
        self.autoscale_view(tight=True)
        return ret
