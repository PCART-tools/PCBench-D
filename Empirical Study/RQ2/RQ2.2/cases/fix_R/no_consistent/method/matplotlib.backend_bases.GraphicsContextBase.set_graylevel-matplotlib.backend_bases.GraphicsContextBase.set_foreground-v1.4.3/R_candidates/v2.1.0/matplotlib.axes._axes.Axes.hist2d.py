    @_preprocess_data(replace_names=["x", "y", "weights"], label_namer=None)
    def hist2d(self, x, y, bins=10, range=None, normed=False, weights=None,
               cmin=None, cmax=None, **kwargs):
        """
        Make a 2D histogram plot.

        Parameters
        ----------
        x, y: array_like, shape (n, )
            Input values

        bins: [None | int | [int, int] | array_like | [array, array]]

            The bin specification:

                - If int, the number of bins for the two dimensions
                  (nx=ny=bins).

                - If [int, int], the number of bins in each dimension
                  (nx, ny = bins).

                - If array_like, the bin edges for the two dimensions
                  (x_edges=y_edges=bins).

                - If [array, array], the bin edges in each dimension
                  (x_edges, y_edges = bins).

            The default value is 10.

        range : array_like shape(2, 2), optional, default: None
             The leftmost and rightmost edges of the bins along each dimension
             (if not specified explicitly in the bins parameters): [[xmin,
             xmax], [ymin, ymax]]. All values outside of this range will be
             considered outliers and not tallied in the histogram.

        normed : boolean, optional, default: False
             Normalize histogram.

        weights : array_like, shape (n, ), optional, default: None
            An array of values w_i weighing each sample (x_i, y_i).

        cmin : scalar, optional, default: None
             All bins that has count less than cmin will not be displayed and
             these count values in the return value count histogram will also
             be set to nan upon return

        cmax : scalar, optional, default: None
             All bins that has count more than cmax will not be displayed (set
             to none before passing to imshow) and these count values in the
             return value count histogram will also be set to nan upon return

        Returns
        -------
        The return value is ``(counts, xedges, yedges, Image)``.

        Other Parameters
        ----------------
        cmap : {Colormap, string}, optional
            A :class:`matplotlib.colors.Colormap` instance.  If not set, use rc
            settings.

        norm : Normalize, optional
            A :class:`matplotlib.colors.Normalize` instance is used to
            scale luminance data to ``[0, 1]``. If not set, defaults to
            ``Normalize()``.

        vmin/vmax : {None, scalar}, optional
            Arguments passed to the `Normalize` instance.

        alpha : ``0 <= scalar <= 1`` or ``None``, optional
            The alpha blending value.

        See also
        --------
        hist : 1D histogram

        Notes
        -----
        Rendering the histogram with a logarithmic color scale is
        accomplished by passing a :class:`colors.LogNorm` instance to
        the *norm* keyword argument. Likewise, power-law normalization
        (similar in effect to gamma correction) can be accomplished with
        :class:`colors.PowerNorm`.
        """

        h, xedges, yedges = np.histogram2d(x, y, bins=bins, range=range,
                                           normed=normed, weights=weights)

        if cmin is not None:
            h[h < cmin] = None
        if cmax is not None:
            h[h > cmax] = None

        pc = self.pcolorfast(xedges, yedges, h.T, **kwargs)
        self.set_xlim(xedges[0], xedges[-1])
        self.set_ylim(yedges[0], yedges[-1])

        return h, xedges, yedges, pc
