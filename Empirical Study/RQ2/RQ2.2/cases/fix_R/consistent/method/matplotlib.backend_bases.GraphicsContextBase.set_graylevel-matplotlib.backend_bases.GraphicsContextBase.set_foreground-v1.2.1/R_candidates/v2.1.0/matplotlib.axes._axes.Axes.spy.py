    def spy(self, Z, precision=0, marker=None, markersize=None,
            aspect='equal', origin="upper", **kwargs):
        """
        Plot the sparsity pattern on a 2-D array.

        ``spy(Z)`` plots the sparsity pattern of the 2-D array *Z*.

        Parameters
        ----------

        Z : sparse array (n, m)
            The array to be plotted.

        precision : float, optional, default: 0
            If *precision* is 0, any non-zero value will be plotted; else,
            values of :math:`|Z| > precision` will be plotted.

            For :class:`scipy.sparse.spmatrix` instances, there is a special
            case: if *precision* is 'present', any value present in the array
            will be plotted, even if it is identically zero.

        origin : ["upper", "lower"], optional, default: "upper"
            Place the [0,0] index of the array in the upper left or lower left
            corner of the axes.

        aspect : ['auto' | 'equal' | scalar], optional, default: "equal"

            If 'equal', and `extent` is None, changes the axes aspect ratio to
            match that of the image. If `extent` is not `None`, the axes
            aspect ratio is changed to match that of the extent.


            If 'auto', changes the image aspect ratio to match that of the
            axes.

            If None, default to rc ``image.aspect`` value.

        Two plotting styles are available: image or marker. Both
        are available for full arrays, but only the marker style
        works for :class:`scipy.sparse.spmatrix` instances.

        If *marker* and *markersize* are *None*, an image will be
        returned and any remaining kwargs are passed to
        :func:`~matplotlib.pyplot.imshow`; else, a
        :class:`~matplotlib.lines.Line2D` object will be returned with
        the value of marker determining the marker type, and any
        remaining kwargs passed to the
        :meth:`~matplotlib.axes.Axes.plot` method.

        If *marker* and *markersize* are *None*, useful kwargs include:

        * *cmap*
        * *alpha*

        See also
        --------
        imshow : for image options.
        plot : for plotting options
        """
        if marker is None and markersize is None and hasattr(Z, 'tocoo'):
            marker = 's'
        if marker is None and markersize is None:
            Z = np.asarray(Z)
            mask = np.abs(Z) > precision

            if 'cmap' not in kwargs:
                kwargs['cmap'] = mcolors.ListedColormap(['w', 'k'],
                                                        name='binary')
            nr, nc = Z.shape
            extent = [-0.5, nc - 0.5, nr - 0.5, -0.5]
            ret = self.imshow(mask, interpolation='nearest', aspect=aspect,
                                extent=extent, origin=origin, **kwargs)
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
            marks = mlines.Line2D(x, y, linestyle='None',
                         marker=marker, markersize=markersize, **kwargs)
            self.add_line(marks)
            nr, nc = Z.shape
            self.set_xlim(xmin=-0.5, xmax=nc - 0.5)
            self.set_ylim(ymin=nr - 0.5, ymax=-0.5)
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
