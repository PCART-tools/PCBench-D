    @_preprocess_data(label_namer=None)
    @docstring.dedent_interpd
    def pcolorfast(self, *args, **kwargs):
        """
        pseudocolor plot of a 2-D array

        Experimental; this is a pcolor-type method that
        provides the fastest possible rendering with the Agg
        backend, and that can handle any quadrilateral grid.
        It supports only flat shading (no outlines), it lacks
        support for log scaling of the axes, and it does not
        have a pyplot wrapper.

        Call signatures::

          ax.pcolorfast(C, **kwargs)
          ax.pcolorfast(xr, yr, C, **kwargs)
          ax.pcolorfast(x, y, C, **kwargs)
          ax.pcolorfast(X, Y, C, **kwargs)

        C is the 2D array of color values corresponding to quadrilateral
        cells. Let (nr, nc) be its shape.  C may be a masked array.

        ``ax.pcolorfast(C, **kwargs)`` is equivalent to
        ``ax.pcolorfast([0,nc], [0,nr], C, **kwargs)``

        *xr*, *yr* specify the ranges of *x* and *y* corresponding to the
        rectangular region bounding *C*.  If::

            xr = [x0, x1]

        and::

            yr = [y0,y1]

        then *x* goes from *x0* to *x1* as the second index of *C* goes
        from 0 to *nc*, etc.  (*x0*, *y0*) is the outermost corner of
        cell (0,0), and (*x1*, *y1*) is the outermost corner of cell
        (*nr*-1, *nc*-1).  All cells are rectangles of the same size.
        This is the fastest version.

        *x*, *y* are monotonic 1D arrays of length *nc* +1 and *nr* +1,
        respectively, giving the x and y boundaries of the cells.  Hence
        the cells are rectangular but the grid may be nonuniform.  The
        speed is intermediate.  (The grid is checked, and if found to be
        uniform the fast version is used.)

        *X* and *Y* are 2D arrays with shape (*nr* +1, *nc* +1) that specify
        the (x,y) coordinates of the corners of the colored
        quadrilaterals; the quadrilateral for C[i,j] has corners at
        (X[i,j],Y[i,j]), (X[i,j+1],Y[i,j+1]), (X[i+1,j],Y[i+1,j]),
        (X[i+1,j+1],Y[i+1,j+1]).  The cells need not be rectangular.
        This is the most general, but the slowest to render.  It may
        produce faster and more compact output using ps, pdf, and
        svg backends, however.

        Note that the column index corresponds to the x-coordinate,
        and the row index corresponds to y; for details, see
        :ref:`Grid Orientation <axes-pcolor-grid-orientation>`.

        Optional keyword arguments:

          *cmap*: [ *None* | Colormap ]
            A :class:`matplotlib.colors.Colormap` instance from cm. If *None*,
            use rc settings.

          *norm*: [ *None* | Normalize ]
            A :class:`matplotlib.colors.Normalize` instance is used to scale
            luminance data to 0,1. If *None*, defaults to normalize()

          *vmin*/*vmax*: [ *None* | scalar ]
            *vmin* and *vmax* are used in conjunction with norm to normalize
            luminance data.  If either are *None*, the min and max
            of the color array *C* is used.  If you pass a norm instance,
            *vmin* and *vmax* will be *None*.

          *alpha*: ``0 <= scalar <= 1``  or *None*
            the alpha blending value

        Return value is an image if a regular or rectangular grid
        is specified, and a :class:`~matplotlib.collections.QuadMesh`
        collection in the general quadrilateral case.

        """

        if not self._hold:
            self.cla()

        alpha = kwargs.pop('alpha', None)
        norm = kwargs.pop('norm', None)
        cmap = kwargs.pop('cmap', None)
        vmin = kwargs.pop('vmin', None)
        vmax = kwargs.pop('vmax', None)
        if norm is not None and not isinstance(norm, mcolors.Normalize):
            msg = "'norm' must be an instance of 'mcolors.Normalize'"
            raise ValueError(msg)

        C = args[-1]
        nr, nc = C.shape
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
            self.add_image(im)
            ret = im

        if vmin is not None or vmax is not None:
            ret.set_clim(vmin, vmax)
        else:
            ret.autoscale_None()

        ret.sticky_edges.x[:] = [xl, xr]
        ret.sticky_edges.y[:] = [yb, yt]
        self.update_datalim(np.array([[xl, yb], [xr, yt]]))
        self.autoscale_view(tight=True)
        return ret
