    @docstring.dedent_interpd
    def spy(self, Z, precision=0, marker=None, markersize=None,
            aspect='equal', origin="upper", **kwargs):
        """
        Plot the sparsity pattern of a 2D array.

        This visualizes the non-zero values of the array.

        Two plotting styles are available: image and marker. Both
        are available for full arrays, but only the marker style
        works for `scipy.sparse.spmatrix` instances.

        **Image style**

        If *marker* and *markersize* are *None*, `~.Axes.imshow` is used. Any
        extra remaining kwargs are passed to this method.

        **Marker style**

        If *Z* is a `scipy.sparse.spmatrix` or *marker* or *markersize* are
        *None*, a `~matplotlib.lines.Line2D` object will be returned with
        the value of marker determining the marker type, and any
        remaining kwargs passed to `~.Axes.plot`.

        Parameters
        ----------
        Z : array-like (M, N)
            The array to be plotted.

        precision : float or 'present', optional, default: 0
            If *precision* is 0, any non-zero value will be plotted. Otherwise,
            values of :math:`|Z| > precision` will be plotted.

            For :class:`scipy.sparse.spmatrix` instances, you can also
            pass 'present'. In this case any value present in the array
            will be plotted, even if it is identically zero.

        origin : {'upper', 'lower'}, optional
            Place the [0,0] index of the array in the upper left or lower left
            corner of the axes. The convention 'upper' is typically used for
            matrices and images.
            If not given, :rc:`image.origin` is used, defaulting to 'upper'.


        aspect : {'equal', 'auto', None} or float, optional
            Controls the aspect ratio of the axes. The aspect is of particular
            relevance for images since it may distort the image, i.e. pixel
            will not be square.

            This parameter is a shortcut for explicitly calling
            `.Axes.set_aspect`. See there for further details.

            - 'equal': Ensures an aspect ratio of 1. Pixels will be square.
            - 'auto': The axes is kept fixed and the aspect is adjusted so
              that the data fit in the axes. In general, this will result in
              non-square pixels.
            - *None*: Use :rc:`image.aspect` (default: 'equal').

            Default: 'equal'

        Returns
        -------
        ret : `~matplotlib.image.AxesImage` or `.Line2D`
            The return type depends on the plotting style (see above).

        Other Parameters
        ----------------
        **kwargs
            The supported additional parameters depend on the plotting style.

            For the image style, you can pass the following additional
            parameters of `~.Axes.imshow`:

            - *cmap*
            - *alpha*
            - *url*
            - any `.Artist` properties (passed on to the `.AxesImage`)

            For the marker style, you can pass any `.Line2D` property except
            for *linestyle*:

        %(_Line2D_docstr)s
        """
        if marker is None and markersize is None and hasattr(Z, 'tocoo'):
            marker = 's'
        if marker is None and markersize is None:
            Z = np.asarray(Z)
            mask = np.abs(Z) > precision

            if 'cmap' not in kwargs:
                kwargs['cmap'] = mcolors.ListedColormap(['w', 'k'],
                                                        name='binary')
            if 'interpolation' in kwargs:
                raise TypeError(
                    "spy() got an unexpected keyword argument 'interpolation'")
            ret = self.imshow(mask, interpolation='nearest', aspect=aspect,
                              origin=origin, **kwargs)
        else:
            if hasattr(Z, 'tocoo'):
                c = Z.tocoo()
                if precision == 'present':
                    y = c.row
                    x = c.col
                else:
                    nonzero = np.abs(c.data) > precision
                    y = c.row[nonzero]
                    x = c.col[nonzero]
            else:
                Z = np.asarray(Z)
                nonzero = np.abs(Z) > precision
                y, x = np.nonzero(nonzero)
            if marker is None:
                marker = 's'
            if markersize is None:
                markersize = 10
            if 'linestyle' in kwargs:
                raise TypeError(
                    "spy() got an unexpected keyword argument 'linestyle'")
            marks = mlines.Line2D(x, y, linestyle='None',
                         marker=marker, markersize=markersize, **kwargs)
            self.add_line(marks)
            nr, nc = Z.shape
            self.set_xlim(-0.5, nc - 0.5)
            self.set_ylim(nr - 0.5, -0.5)
            self.set_aspect(aspect)
            ret = marks
        self.title.set_y(1.05)
        self.xaxis.tick_top()
        self.xaxis.set_ticks_position('both')
        self.xaxis.set_major_locator(mticker.MaxNLocator(nbins=9,
                                                 steps=[1, 2, 5, 10],
                                                 integer=True))
        self.yaxis.set_major_locator(mticker.MaxNLocator(nbins=9,
                                                 steps=[1, 2, 5, 10],
                                                 integer=True))
        return ret
