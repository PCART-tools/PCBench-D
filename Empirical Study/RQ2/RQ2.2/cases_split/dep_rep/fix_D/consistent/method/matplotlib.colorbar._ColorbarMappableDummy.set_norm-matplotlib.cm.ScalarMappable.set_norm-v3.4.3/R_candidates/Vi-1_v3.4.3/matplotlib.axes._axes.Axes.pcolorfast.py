    @_preprocess_data()
    @docstring.dedent_interpd
    def pcolorfast(self, *args, alpha=None, norm=None, cmap=None, vmin=None,
                   vmax=None, **kwargs):
        """
        Create a pseudocolor plot with a non-regular rectangular grid.

        Call signature::

          ax.pcolorfast([X, Y], C, /, **kwargs)

        This method is similar to `~.Axes.pcolor` and `~.Axes.pcolormesh`.
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
        C : array-like
            The image data. Supported array shapes are:

            - (M, N): an image with scalar data. The data is visualized
              using a colormap.
            - (M, N, 3): an image with RGB values (0-1 float or 0-255 int).
            - (M, N, 4): an image with RGBA values (0-1 float or 0-255 int),
              i.e. including transparency.

            The first two dimensions (M, N) define the rows and columns of
            the image.

            This parameter can only be passed positionally.

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

              In this case *X* and *Y* are 2D arrays with shape (M + 1, N + 1),
              specifying the x and y coordinates of the corners of the colored
              quadrilaterals.

              This is the most general, but the slowest to render.  It may
              produce faster and more compact output using ps, pdf, and
              svg backends, however.

            These arguments can only be passed positionally.

        cmap : str or `~matplotlib.colors.Colormap`, default: :rc:`image.cmap`
            A Colormap instance or registered colormap name. The colormap
            maps the *C* values to colors.

        norm : `~matplotlib.colors.Normalize`, optional
            The Normalize instance scales the data values to the canonical
            colormap range [0, 1] for mapping to colors. By default, the data
            range is mapped to the colorbar range using linear scaling.

        vmin, vmax : float, default: None
            The colorbar range. If *None*, suitable min/max values are
            automatically chosen by the `~.Normalize` instance (defaults to
            the respective min/max values of *C* in case of the default linear
            scaling).
            It is deprecated to use *vmin*/*vmax* when *norm* is given.

        alpha : float, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        snap : bool, default: False
            Whether to snap the mesh to pixel boundaries.

        Returns
        -------
        `.AxesImage` or `.PcolorImage` or `.QuadMesh`
            The return type depends on the type of grid:

            - `.AxesImage` for a regular rectangular grid.
            - `.PcolorImage` for a non-regular rectangular grid.
            - `.QuadMesh` for a non-rectangular grid.

        Other Parameters
        ----------------
        **kwargs
            Supported additional parameters depend on the type of grid.
            See return types of *image* for further description.

        Notes
        -----
        .. [notes section required to get data note injection right]
        """

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
                    if (np.ptp(dx) < 0.01 * abs(dx.mean()) and
                            np.ptp(dy) < 0.01 * abs(dy.mean())):
                        style = "image"
                    else:
                        style = "pcolorimage"
            elif x.ndim == 2 and y.ndim == 2:
                style = "quadmesh"
            else:
                raise TypeError("arguments do not match valid signatures")
        else:
            raise TypeError("need 1 argument or 3 arguments")

        if style == "quadmesh":
            # data point in each cell is value at lower left corner
            coords = np.stack([x, y], axis=-1)
            if np.ndim(C) == 2:
                qm_kwargs = {"array": np.ma.ravel(C)}
            elif np.ndim(C) == 3:
                qm_kwargs = {"color": np.ma.reshape(C, (-1, C.shape[-1]))}
            else:
                raise ValueError("C must be 2D or 3D")
            collection = mcoll.QuadMesh(
                nc, nr, coords, **qm_kwargs,
                alpha=alpha, cmap=cmap, norm=norm,
                antialiased=False, edgecolors="none")
            self.add_collection(collection, autolim=False)
            xl, xr, yb, yt = x.min(), x.max(), y.min(), y.max()
            ret = collection

        else:  # It's one of the two image styles.
            extent = xl, xr, yb, yt = x[0], x[-1], y[0], y[-1]
            if style == "image":
                im = mimage.AxesImage(
                    self, cmap, norm,
                    data=C, alpha=alpha, extent=extent,
                    interpolation='nearest', origin='lower',
                    **kwargs)
            elif style == "pcolorimage":
                im = mimage.PcolorImage(
                    self, x, y, C,
                    cmap=cmap, norm=norm, alpha=alpha, extent=extent,
                    **kwargs)
            self.add_image(im)
            ret = im

        if np.ndim(C) == 2:  # C.ndim == 3 is RGB(A) so doesn't need scaling.
            ret._scale_norm(norm, vmin, vmax)

        if ret.get_clip_path() is None:
            # image does not already have clipping set, clip to axes patch
            ret.set_clip_path(self.patch)

        ret.sticky_edges.x[:] = [xl, xr]
        ret.sticky_edges.y[:] = [yb, yt]
        self.update_datalim(np.array([[xl, yb], [xr, yt]]))
        self._request_autoscale_view(tight=True)
        return ret
