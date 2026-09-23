    def figimage(self, X, xo=0, yo=0, alpha=None, norm=None, cmap=None,
                 vmin=None, vmax=None, origin=None, resize=False, **kwargs):
        """
        Add a non-resampled image to the figure.

        The image is attached to the lower or upper left corner depending on
        *origin*.

        Parameters
        ----------
        X
            The image data. This is an array of one of the following shapes:

            - MxN: luminance (grayscale) values
            - MxNx3: RGB values
            - MxNx4: RGBA values

        xo, yo : int
            The *x*/*y* image offset in pixels.

        alpha : None or float
            The alpha blending value.

        norm : :class:`matplotlib.colors.Normalize`
            A :class:`.Normalize` instance to map the luminance to the
            interval [0, 1].

        cmap : str or :class:`matplotlib.colors.Colormap`
            The colormap to use. Default: :rc:`image.cmap`.

        vmin, vmax : scalar
            If *norm* is not given, these values set the data limits for the
            colormap.

        origin : {'upper', 'lower'}
            Indicates where the [0, 0] index of the array is in the upper left
            or lower left corner of the axes. Defaults to :rc:`image.origin`.

        resize : bool
            If *True*, resize the figure to match the given image size.

        Returns
        -------
        :class:`matplotlib.image.FigureImage`

        Other Parameters
        ----------------
        **kwargs
            Additional kwargs are `.Artist` kwargs passed on to `.FigureImage`.

        Notes
        -----
        figimage complements the axes image
        (:meth:`~matplotlib.axes.Axes.imshow`) which will be resampled
        to fit the current axes.  If you want a resampled image to
        fill the entire figure, you can define an
        :class:`~matplotlib.axes.Axes` with extent [0,0,1,1].


        Examples::

            f = plt.figure()
            nx = int(f.get_figwidth() * f.dpi)
            ny = int(f.get_figheight() * f.dpi)
            data = np.random.random((ny, nx))
            f.figimage(data)
            plt.show()

        """
        if resize:
            dpi = self.get_dpi()
            figsize = [x / dpi for x in (X.shape[1], X.shape[0])]
            self.set_size_inches(figsize, forward=True)

        im = mimage.FigureImage(self, cmap, norm, xo, yo, origin, **kwargs)
        im.stale_callback = _stale_figure_callback

        im.set_array(X)
        im.set_alpha(alpha)
        if norm is None:
            im.set_clim(vmin, vmax)
        self.images.append(im)
        im._remove_method = self.images.remove
        self.stale = True
        return im
