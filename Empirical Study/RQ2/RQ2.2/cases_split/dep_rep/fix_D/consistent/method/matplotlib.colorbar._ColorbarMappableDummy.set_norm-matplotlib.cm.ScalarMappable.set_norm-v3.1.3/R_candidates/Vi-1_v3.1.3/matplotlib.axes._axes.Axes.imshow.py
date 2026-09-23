    @_preprocess_data()
    @cbook._delete_parameter("3.1", "shape")
    @cbook._delete_parameter("3.1", "imlim")
    def imshow(self, X, cmap=None, norm=None, aspect=None,
               interpolation=None, alpha=None, vmin=None, vmax=None,
               origin=None, extent=None, shape=None, filternorm=1,
               filterrad=4.0, imlim=None, resample=None, url=None, **kwargs):
        """
        Display an image, i.e. data on a 2D regular raster.

        Parameters
        ----------
        X : array-like or PIL image
            The image data. Supported array shapes are:

            - (M, N): an image with scalar data. The data is visualized
              using a colormap.
            - (M, N, 3): an image with RGB values (0-1 float or 0-255 int).
            - (M, N, 4): an image with RGBA values (0-1 float or 0-255 int),
              i.e. including transparency.

            The first two dimensions (M, N) define the rows and columns of
            the image.

            Out-of-range RGB(A) values are clipped.

        cmap : str or `~matplotlib.colors.Colormap`, optional
            The Colormap instance or registered colormap name used to map
            scalar data to colors. This parameter is ignored for RGB(A) data.
            Defaults to :rc:`image.cmap`.

        norm : `~matplotlib.colors.Normalize`, optional
            The `Normalize` instance used to scale scalar data to the [0, 1]
            range before mapping to colors using *cmap*. By default, a linear
            scaling mapping the lowest value to 0 and the highest to 1 is used.
            This parameter is ignored for RGB(A) data.

        aspect : {'equal', 'auto'} or float, optional
            Controls the aspect ratio of the axes. The aspect is of particular
            relevance for images since it may distort the image, i.e. pixel
            will not be square.

            This parameter is a shortcut for explicitly calling
            `.Axes.set_aspect`. See there for further details.

            - 'equal': Ensures an aspect ratio of 1. Pixels will be square
              (unless pixel sizes are explicitly made non-square in data
              coordinates using *extent*).
            - 'auto': The axes is kept fixed and the aspect is adjusted so
              that the data fit in the axes. In general, this will result in
              non-square pixels.

            If not given, use :rc:`image.aspect` (default: 'equal').

        interpolation : str, optional
            The interpolation method used. If *None*
            :rc:`image.interpolation` is used, which defaults to 'nearest'.

            Supported values are 'none', 'nearest', 'bilinear', 'bicubic',
            'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser',
            'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc',
            'lanczos'.

            If *interpolation* is 'none', then no interpolation is performed
            on the Agg, ps, pdf and svg backends. Other backends will fall back
            to 'nearest'. Note that most SVG renders perform interpolation at
            rendering and that the default interpolation method they implement
            may differ.

            See
            :doc:`/gallery/images_contours_and_fields/interpolation_methods`
            for an overview of the supported interpolation methods.

            Some interpolation methods require an additional radius parameter,
            which can be set by *filterrad*. Additionally, the antigrain image
            resize filter is controlled by the parameter *filternorm*.

        alpha : scalar, optional
            The alpha blending value, between 0 (transparent) and 1 (opaque).
            This parameter is ignored for RGBA input data.

        vmin, vmax : scalar, optional
            When using scalar data and no explicit *norm*, *vmin* and *vmax*
            define the data range that the colormap covers. By default,
            the colormap covers the complete value range of the supplied
            data. *vmin*, *vmax* are ignored if the *norm* parameter is used.

        origin : {'upper', 'lower'}, optional
            Place the [0,0] index of the array in the upper left or lower left
            corner of the axes. The convention 'upper' is typically used for
            matrices and images.
            If not given, :rc:`image.origin` is used, defaulting to 'upper'.

            Note that the vertical axes points upward for 'lower'
            but downward for 'upper'.

            See the :doc:`/tutorials/intermediate/imshow_extent` tutorial for
            examples and a more detailed description.

        extent : scalars (left, right, bottom, top), optional
            The bounding box in data coordinates that the image will fill.
            The image is stretched individually along x and y to fill the box.

            The default extent is determined by the following conditions.
            Pixels have unit size in data coordinates. Their centers are on
            integer coordinates, and their center coordinates range from 0 to
            columns-1 horizontally and from 0 to rows-1 vertically.

            Note that the direction of the vertical axis and thus the default
            values for top and bottom depend on *origin*:

            - For ``origin == 'upper'`` the default is
              ``(-0.5, numcols-0.5, numrows-0.5, -0.5)``.
            - For ``origin == 'lower'`` the default is
              ``(-0.5, numcols-0.5, -0.5, numrows-0.5)``.

            See the :doc:`/tutorials/intermediate/imshow_extent` tutorial for
            examples and a more detailed description.

        filternorm : bool, optional, default: True
            A parameter for the antigrain image resize filter (see the
            antigrain documentation).  If *filternorm* is set, the filter
            normalizes integer values and corrects the rounding errors. It
            doesn't do anything with the source floating point values, it
            corrects only integers according to the rule of 1.0 which means
            that any sum of pixel weights must be equal to 1.0.  So, the
            filter function must produce a graph of the proper shape.

        filterrad : float > 0, optional, default: 4.0
            The filter radius for filters that have a radius parameter, i.e.
            when interpolation is one of: 'sinc', 'lanczos' or 'blackman'.

        resample : bool, optional
            When *True*, use a full resampling method.  When *False*, only
            resample when the output image is larger than the input image.

        url : str, optional
            Set the url of the created `.AxesImage`. See `.Artist.set_url`.

        Returns
        -------
        image : `~matplotlib.image.AxesImage`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.artist.Artist` properties
            These parameters are passed on to the constructor of the
            `.AxesImage` artist.

        See also
        --------
        matshow : Plot a matrix or an array as an image.

        Notes
        -----
        Unless *extent* is used, pixel centers will be located at integer
        coordinates. In other words: the origin will coincide with the center
        of pixel (0, 0).

        There are two common representations for RGB images with an alpha
        channel:

        -   Straight (unassociated) alpha: R, G, and B channels represent the
            color of the pixel, disregarding its opacity.
        -   Premultiplied (associated) alpha: R, G, and B channels represent
            the color of the pixel, adjusted for its opacity by multiplication.

        `~matplotlib.pyplot.imshow` expects RGB images adopting the straight
        (unassociated) alpha representation.
        """
        if norm is not None and not isinstance(norm, mcolors.Normalize):
            raise ValueError(
                "'norm' must be an instance of 'mcolors.Normalize'")
        if aspect is None:
            aspect = rcParams['image.aspect']
        self.set_aspect(aspect)
        im = mimage.AxesImage(self, cmap, norm, interpolation, origin, extent,
                              filternorm=filternorm, filterrad=filterrad,
                              resample=resample, **kwargs)

        im.set_data(X)
        im.set_alpha(alpha)
        if im.get_clip_path() is None:
            # image does not already have clipping set, clip to axes patch
            im.set_clip_path(self.patch)
        if vmin is not None or vmax is not None:
            im.set_clim(vmin, vmax)
        else:
            im.autoscale_None()
        im.set_url(url)

        # update ax.dataLim, and, if autoscaling, set viewLim
        # to tightly fit the image, regardless of dataLim.
        im.set_extent(im.get_extent())

        self.add_image(im)
        return im
