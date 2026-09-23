class Figure(FigureBase):
    """
    The top level container for all the plot elements.

    The Figure instance supports callbacks through a *callbacks* attribute
    which is a `.CallbackRegistry` instance.  The events you can connect to
    are 'dpi_changed', and the callback will be called with ``func(fig)`` where
    fig is the `Figure` instance.

    Attributes
    ----------
    patch
        The `.Rectangle` instance representing the figure background patch.

    suppressComposite
        For multiple figure images, the figure will make composite images
        depending on the renderer option_image_nocomposite function.  If
        *suppressComposite* is a boolean, this will override the renderer.
    """

    def __str__(self):
        return "Figure(%gx%g)" % tuple(self.bbox.size)

    def __repr__(self):
        return "<{clsname} size {h:g}x{w:g} with {naxes} Axes>".format(
            clsname=self.__class__.__name__,
            h=self.bbox.size[0], w=self.bbox.size[1],
            naxes=len(self.axes),
        )

    def __init__(self,
                 figsize=None,
                 dpi=None,
                 facecolor=None,
                 edgecolor=None,
                 linewidth=0.0,
                 frameon=None,
                 subplotpars=None,  # rc figure.subplot.*
                 tight_layout=None,  # rc figure.autolayout
                 constrained_layout=None,  # rc figure.constrained_layout.use
                 ):
        """
        Parameters
        ----------
        figsize : 2-tuple of floats, default: :rc:`figure.figsize`
            Figure dimension ``(width, height)`` in inches.

        dpi : float, default: :rc:`figure.dpi`
            Dots per inch.

        facecolor : default: :rc:`figure.facecolor`
            The figure patch facecolor.

        edgecolor : default: :rc:`figure.edgecolor`
            The figure patch edge color.

        linewidth : float
            The linewidth of the frame (i.e. the edge linewidth of the figure
            patch).

        frameon : bool, default: :rc:`figure.frameon`
            If ``False``, suppress drawing the figure background patch.

        subplotpars : `SubplotParams`
            Subplot parameters. If not given, the default subplot
            parameters :rc:`figure.subplot.*` are used.

        tight_layout : bool or dict, default: :rc:`figure.autolayout`
            If ``False`` use *subplotpars*. If ``True`` adjust subplot
            parameters using `.tight_layout` with default padding.
            When providing a dict containing the keys ``pad``, ``w_pad``,
            ``h_pad``, and ``rect``, the default `.tight_layout` paddings
            will be overridden.

        constrained_layout : bool, default: :rc:`figure.constrained_layout.use`
            If ``True`` use constrained layout to adjust positioning of plot
            elements.  Like ``tight_layout``, but designed to be more
            flexible.  See
            :doc:`/tutorials/intermediate/constrainedlayout_guide`
            for examples.  (Note: does not work with `add_subplot` or
            `~.pyplot.subplot2grid`.)
        """
        super().__init__()

        self.callbacks = cbook.CallbackRegistry()
        # Callbacks traditionally associated with the canvas (and exposed with
        # a proxy property), but that actually need to be on the figure for
        # pickling.
        self._canvas_callbacks = cbook.CallbackRegistry()
        self._button_pick_id = self._canvas_callbacks.connect(
            'button_press_event', lambda event: self.canvas.pick(event))
        self._scroll_pick_id = self._canvas_callbacks.connect(
            'scroll_event', lambda event: self.canvas.pick(event))

        if figsize is None:
            figsize = mpl.rcParams['figure.figsize']
        if dpi is None:
            dpi = mpl.rcParams['figure.dpi']
        if facecolor is None:
            facecolor = mpl.rcParams['figure.facecolor']
        if edgecolor is None:
            edgecolor = mpl.rcParams['figure.edgecolor']
        if frameon is None:
            frameon = mpl.rcParams['figure.frameon']

        if not np.isfinite(figsize).all() or (np.array(figsize) < 0).any():
            raise ValueError('figure size must be positive finite not '
                             f'{figsize}')
        self.bbox_inches = Bbox.from_bounds(0, 0, *figsize)

        self.dpi_scale_trans = Affine2D().scale(dpi)
        # do not use property as it will trigger
        self._dpi = dpi
        self.bbox = TransformedBbox(self.bbox_inches, self.dpi_scale_trans)
        self.figbbox = self.bbox
        self.transFigure = BboxTransformTo(self.bbox)
        self.transSubfigure = self.transFigure

        self.patch = Rectangle(
            xy=(0, 0), width=1, height=1, visible=frameon,
            facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
            # Don't let the figure patch influence bbox calculation.
            in_layout=False)
        self._set_artist_props(self.patch)
        self.patch.set_antialiased(False)

        FigureCanvasBase(self)  # Set self.canvas.

        if subplotpars is None:
            subplotpars = SubplotParams()

        self.subplotpars = subplotpars

        # constrained_layout:
        self._layoutgrid = None
        self._constrained = False

        self.set_tight_layout(tight_layout)

        self._axstack = _AxesStack()  # track all figure axes and current axes
        self.clf()
        self._cachedRenderer = None

        self.set_constrained_layout(constrained_layout)

        # list of child gridspecs for this figure
        self._gridspecs = []

    # TODO: I'd like to dynamically add the _repr_html_ method
    # to the figure in the right context, but then IPython doesn't
    # use it, for some reason.

    def _repr_html_(self):
        # We can't use "isinstance" here, because then we'd end up importing
        # webagg unconditionally.
        if 'WebAgg' in type(self.canvas).__name__:
            from matplotlib.backends import backend_webagg
            return backend_webagg.ipython_inline_display(self)

    def show(self, warn=True):
        """
        If using a GUI backend with pyplot, display the figure window.

        If the figure was not created using `~.pyplot.figure`, it will lack
        a `~.backend_bases.FigureManagerBase`, and this method will raise an
        AttributeError.

        .. warning::

            This does not manage an GUI event loop. Consequently, the figure
            may only be shown briefly or not shown at all if you or your
            environment are not managing an event loop.

            Proper use cases for `.Figure.show` include running this from a
            GUI application or an IPython shell.

            If you're running a pure python shell or executing a non-GUI
            python script, you should use `matplotlib.pyplot.show` instead,
            which takes care of managing the event loop for you.

        Parameters
        ----------
        warn : bool, default: True
            If ``True`` and we are not running headless (i.e. on Linux with an
            unset DISPLAY), issue warning when called on a non-GUI backend.
        """
        if self.canvas.manager is None:
            raise AttributeError(
                "Figure.show works only for figures managed by pyplot, "
                "normally created by pyplot.figure()")
        try:
            self.canvas.manager.show()
        except NonGuiException as exc:
            if warn:
                _api.warn_external(str(exc))

    def get_axes(self):
        """
        Return a list of Axes in the Figure. You can access and modify the
        Axes in the Figure through this list.

        Do not modify the list itself. Instead, use `~Figure.add_axes`,
        `~.Figure.add_subplot` or `~.Figure.delaxes` to add or remove an Axes.

        Note: This is equivalent to the property `~.Figure.axes`.
        """
        return self._axstack.as_list()

    axes = property(get_axes, doc="""
        List of Axes in the Figure.  You can access and modify the Axes in the
        Figure through this list.

        Do not modify the list itself. Instead, use "`~Figure.add_axes`,
        `~.Figure.add_subplot` or `~.Figure.delaxes` to add or remove an Axes.
        """)

    def _get_dpi(self):
        return self._dpi

    def _set_dpi(self, dpi, forward=True):
        """
        Parameters
        ----------
        dpi : float

        forward : bool
            Passed on to `~.Figure.set_size_inches`
        """
        if dpi == self._dpi:
            # We don't want to cause undue events in backends.
            return
        self._dpi = dpi
        self.dpi_scale_trans.clear().scale(dpi)
        w, h = self.get_size_inches()
        self.set_size_inches(w, h, forward=forward)
        self.callbacks.process('dpi_changed', self)

    dpi = property(_get_dpi, _set_dpi, doc="The resolution in dots per inch.")

    def get_tight_layout(self):
        """Return whether `.tight_layout` is called when drawing."""
        return self._tight

    def set_tight_layout(self, tight):
        """
        Set whether and how `.tight_layout` is called when drawing.

        Parameters
        ----------
        tight : bool or dict with keys "pad", "w_pad", "h_pad", "rect" or None
            If a bool, sets whether to call `.tight_layout` upon drawing.
            If ``None``, use the ``figure.autolayout`` rcparam instead.
            If a dict, pass it as kwargs to `.tight_layout`, overriding the
            default paddings.
        """
        if tight is None:
            tight = mpl.rcParams['figure.autolayout']
        self._tight = bool(tight)
        self._tight_parameters = tight if isinstance(tight, dict) else {}
        self.stale = True

    def get_constrained_layout(self):
        """
        Return whether constrained layout is being used.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.
        """
        return self._constrained

    def set_constrained_layout(self, constrained):
        """
        Set whether ``constrained_layout`` is used upon drawing. If None,
        :rc:`figure.constrained_layout.use` value will be used.

        When providing a dict containing the keys `w_pad`, `h_pad`
        the default ``constrained_layout`` paddings will be
        overridden.  These pads are in inches and default to 3.0/72.0.
        ``w_pad`` is the width padding and ``h_pad`` is the height padding.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.

        Parameters
        ----------
        constrained : bool or dict or None
        """
        self._constrained_layout_pads = dict()
        self._constrained_layout_pads['w_pad'] = None
        self._constrained_layout_pads['h_pad'] = None
        self._constrained_layout_pads['wspace'] = None
        self._constrained_layout_pads['hspace'] = None
        if constrained is None:
            constrained = mpl.rcParams['figure.constrained_layout.use']
        self._constrained = bool(constrained)
        if isinstance(constrained, dict):
            self.set_constrained_layout_pads(**constrained)
        else:
            self.set_constrained_layout_pads()

        self.init_layoutgrid()

        self.stale = True

    def set_constrained_layout_pads(self, **kwargs):
        """
        Set padding for ``constrained_layout``.  Note the kwargs can be passed
        as a dictionary ``fig.set_constrained_layout(**paddict)``.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.

        Parameters
        ----------
        w_pad : float
            Width padding in inches.  This is the pad around Axes
            and is meant to make sure there is enough room for fonts to
            look good.  Defaults to 3 pts = 0.04167 inches

        h_pad : float
            Height padding in inches. Defaults to 3 pts.

        wspace : float
            Width padding between subplots, expressed as a fraction of the
            subplot width.  The total padding ends up being w_pad + wspace.

        hspace : float
            Height padding between subplots, expressed as a fraction of the
            subplot width. The total padding ends up being h_pad + hspace.

        """

        todo = ['w_pad', 'h_pad', 'wspace', 'hspace']
        for td in todo:
            if td in kwargs and kwargs[td] is not None:
                self._constrained_layout_pads[td] = kwargs[td]
            else:
                self._constrained_layout_pads[td] = (
                    mpl.rcParams['figure.constrained_layout.' + td])

    def get_constrained_layout_pads(self, relative=False):
        """
        Get padding for ``constrained_layout``.

        Returns a list of ``w_pad, h_pad`` in inches and
        ``wspace`` and ``hspace`` as fractions of the subplot.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.

        Parameters
        ----------
        relative : bool
            If `True`, then convert from inches to figure relative.
        """
        w_pad = self._constrained_layout_pads['w_pad']
        h_pad = self._constrained_layout_pads['h_pad']
        wspace = self._constrained_layout_pads['wspace']
        hspace = self._constrained_layout_pads['hspace']

        if relative and (w_pad is not None or h_pad is not None):
            renderer0 = layoutgrid.get_renderer(self)
            dpi = renderer0.dpi
            w_pad = w_pad * dpi / renderer0.width
            h_pad = h_pad * dpi / renderer0.height

        return w_pad, h_pad, wspace, hspace

    def set_canvas(self, canvas):
        """
        Set the canvas that contains the figure

        Parameters
        ----------
        canvas : FigureCanvas
        """
        self.canvas = canvas

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

        norm : `matplotlib.colors.Normalize`
            A `.Normalize` instance to map the luminance to the
            interval [0, 1].

        cmap : str or `matplotlib.colors.Colormap`, default: :rc:`image.cmap`
            The colormap to use.

        vmin, vmax : float
            If *norm* is not given, these values set the data limits for the
            colormap.

        origin : {'upper', 'lower'}, default: :rc:`image.origin`
            Indicates where the [0, 0] index of the array is in the upper left
            or lower left corner of the axes.

        resize : bool
            If *True*, resize the figure to match the given image size.

        Returns
        -------
        `matplotlib.image.FigureImage`

        Other Parameters
        ----------------
        **kwargs
            Additional kwargs are `.Artist` kwargs passed on to `.FigureImage`.

        Notes
        -----
        figimage complements the Axes image (`~matplotlib.axes.Axes.imshow`)
        which will be resampled to fit the current Axes.  If you want
        a resampled image to fill the entire figure, you can define an
        `~matplotlib.axes.Axes` with extent [0, 0, 1, 1].

        Examples
        --------
        ::

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

    def set_size_inches(self, w, h=None, forward=True):
        """
        Set the figure size in inches.

        Call signatures::

             fig.set_size_inches(w, h)  # OR
             fig.set_size_inches((w, h))

        Parameters
        ----------
        w : (float, float) or float
            Width and height in inches (if height not specified as a separate
            argument) or width.
        h : float
            Height in inches.
        forward : bool, default: True
            If ``True``, the canvas size is automatically updated, e.g.,
            you can resize the figure window from the shell.

        See Also
        --------
        matplotlib.figure.Figure.get_size_inches
        matplotlib.figure.Figure.set_figwidth
        matplotlib.figure.Figure.set_figheight

        Notes
        -----
        To transform from pixels to inches divide by `Figure.dpi`.
        """
        if h is None:  # Got called with a single pair as argument.
            w, h = w
        size = np.array([w, h])
        if not np.isfinite(size).all() or (size < 0).any():
            raise ValueError(f'figure size must be positive finite not {size}')
        self.bbox_inches.p1 = size
        if forward:
            canvas = getattr(self, 'canvas')
            if canvas is not None:
                dpi_ratio = getattr(canvas, '_dpi_ratio', 1)
                manager = getattr(canvas, 'manager', None)
                if manager is not None:
                    manager.resize(*(size * self.dpi / dpi_ratio).astype(int))
        self.stale = True

    def get_size_inches(self):
        """
        Return the current size of the figure in inches.

        Returns
        -------
        ndarray
           The size (width, height) of the figure in inches.

        See Also
        --------
        matplotlib.figure.Figure.set_size_inches
        matplotlib.figure.Figure.get_figwidth
        matplotlib.figure.Figure.get_figheight

        Notes
        -----
        The size in pixels can be obtained by multiplying with `Figure.dpi`.
        """
        return np.array(self.bbox_inches.p1)

    def get_figwidth(self):
        """Return the figure width in inches."""
        return self.bbox_inches.width

    def get_figheight(self):
        """Return the figure height in inches."""
        return self.bbox_inches.height

    def get_dpi(self):
        """Return the resolution in dots per inch as a float."""
        return self.dpi

    def set_dpi(self, val):
        """
        Set the resolution of the figure in dots-per-inch.

        Parameters
        ----------
        val : float
        """
        self.dpi = val
        self.stale = True

    def set_figwidth(self, val, forward=True):
        """
        Set the width of the figure in inches.

        Parameters
        ----------
        val : float
        forward : bool
            See `set_size_inches`.

        See Also
        --------
        matplotlib.figure.Figure.set_figheight
        matplotlib.figure.Figure.set_size_inches
        """
        self.set_size_inches(val, self.get_figheight(), forward=forward)

    def set_figheight(self, val, forward=True):
        """
        Set the height of the figure in inches.

        Parameters
        ----------
        val : float
        forward : bool
            See `set_size_inches`.

        See Also
        --------
        matplotlib.figure.Figure.set_figwidth
        matplotlib.figure.Figure.set_size_inches
        """
        self.set_size_inches(self.get_figwidth(), val, forward=forward)

    def clf(self, keep_observers=False):
        """
        Clear the figure.

        Set *keep_observers* to True if, for example,
        a gui widget is tracking the Axes in the figure.
        """
        self.suppressComposite = None
        self.callbacks = cbook.CallbackRegistry()

        for ax in tuple(self.axes):  # Iterate over the copy.
            ax.cla()
            self.delaxes(ax)         # removes ax from self._axstack

        toolbar = getattr(self.canvas, 'toolbar', None)
        if toolbar is not None:
            toolbar.update()
        self._axstack.clear()
        self.artists = []
        self.lines = []
        self.patches = []
        self.texts = []
        self.images = []
        self.legends = []
        if not keep_observers:
            self._axobservers = cbook.CallbackRegistry()
        self._suptitle = None
        self._supxlabel = None
        self._supylabel = None

        if self.get_constrained_layout():
            self.init_layoutgrid()
        self.stale = True

    def clear(self, keep_observers=False):
        """Clear the figure -- synonym for `clf`."""
        self.clf(keep_observers=keep_observers)

    @_finalize_rasterization
    @allow_rasterization
    def draw(self, renderer):
        # docstring inherited
        self._cachedRenderer = renderer

        # draw the figure bounding box, perhaps none for white figure
        if not self.get_visible():
            return

        artists = self._get_draw_artists(renderer)

        try:
            renderer.open_group('figure', gid=self.get_gid())
            if self.get_constrained_layout() and self.axes:
                self.execute_constrained_layout(renderer)
            if self.get_tight_layout() and self.axes:
                try:
                    self.tight_layout(**self._tight_parameters)
                except ValueError:
                    pass
                    # ValueError can occur when resizing a window.

            self.patch.draw(renderer)
            mimage._draw_list_compositing_images(
                renderer, self, artists, self.suppressComposite)

            for sfig in self.subfigs:
                sfig.draw(renderer)

            renderer.close_group('figure')
        finally:
            self.stale = False

        self.canvas.draw_event(renderer)

    def draw_artist(self, a):
        """
        Draw `.Artist` *a* only.

        This method can only be used after an initial draw of the figure,
        because that creates and caches the renderer needed here.
        """
        if self._cachedRenderer is None:
            raise AttributeError("draw_artist can only be used after an "
                                 "initial draw which caches the renderer")
        a.draw(self._cachedRenderer)

    def __getstate__(self):
        state = super().__getstate__()

        # The canvas cannot currently be pickled, but this has the benefit
        # of meaning that a figure can be detached from one canvas, and
        # re-attached to another.
        state.pop("canvas")

        # Set cached renderer to None -- it can't be pickled.
        state["_cachedRenderer"] = None

        # add version information to the state
        state['__mpl_version__'] = _mpl_version

        # check whether the figure manager (if any) is registered with pyplot
        from matplotlib import _pylab_helpers
        if getattr(self.canvas, 'manager', None) \
                in _pylab_helpers.Gcf.figs.values():
            state['_restore_to_pylab'] = True

        # set all the layoutgrid information to None.  kiwisolver objects can't
        # be pickled, so we lose the layout options at this point.
        state.pop('_layoutgrid', None)

        return state

    def __setstate__(self, state):
        version = state.pop('__mpl_version__')
        restore_to_pylab = state.pop('_restore_to_pylab', False)

        if version != _mpl_version:
            _api.warn_external(
                f"This figure was saved with matplotlib version {version} and "
                f"is unlikely to function correctly.")

        self.__dict__ = state

        # re-initialise some of the unstored state information
        FigureCanvasBase(self)  # Set self.canvas.
        self._layoutgrid = None

        if restore_to_pylab:
            # lazy import to avoid circularity
            import matplotlib.pyplot as plt
            import matplotlib._pylab_helpers as pylab_helpers
            allnums = plt.get_fignums()
            num = max(allnums) + 1 if allnums else 1
            mgr = plt._backend_mod.new_figure_manager_given_figure(num, self)
            pylab_helpers.Gcf._set_new_active_manager(mgr)
            plt.draw_if_interactive()

        self.stale = True

    def add_axobserver(self, func):
        """Whenever the Axes state change, ``func(self)`` will be called."""
        # Connect a wrapper lambda and not func itself, to avoid it being
        # weakref-collected.
        self._axobservers.connect("_axes_change_event", lambda arg: func(arg))

    def savefig(self, fname, *, transparent=None, **kwargs):
        """
        Save the current figure.

        Call signature::

          savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                  orientation='portrait', papertype=None, format=None,
                  transparent=False, bbox_inches=None, pad_inches=0.1,
                  frameon=None, metadata=None)

        The available output formats depend on the backend being used.

        Parameters
        ----------
        fname : str or path-like or binary file-like
            A path, or a Python file-like object, or
            possibly some backend-dependent object such as
            `matplotlib.backends.backend_pdf.PdfPages`.

            If *format* is set, it determines the output format, and the file
            is saved as *fname*.  Note that *fname* is used verbatim, and there
            is no attempt to make the extension, if any, of *fname* match
            *format*, and no extension is appended.

            If *format* is not set, then the format is inferred from the
            extension of *fname*, if there is one.  If *format* is not
            set and *fname* has no extension, then the file is saved with
            :rc:`savefig.format` and the appropriate extension is appended to
            *fname*.

        Other Parameters
        ----------------
        dpi : float or 'figure', default: :rc:`savefig.dpi`
            The resolution in dots per inch.  If 'figure', use the figure's
            dpi value.

        quality : int, default: :rc:`savefig.jpeg_quality`
            Applicable only if *format* is 'jpg' or 'jpeg', ignored otherwise.

            The image quality, on a scale from 1 (worst) to 95 (best).
            Values above 95 should be avoided; 100 disables portions of
            the JPEG compression algorithm, and results in large files
            with hardly any gain in image quality.

            This parameter is deprecated.

        optimize : bool, default: False
            Applicable only if *format* is 'jpg' or 'jpeg', ignored otherwise.

            Whether the encoder should make an extra pass over the image
            in order to select optimal encoder settings.

            This parameter is deprecated.

        progressive : bool, default: False
            Applicable only if *format* is 'jpg' or 'jpeg', ignored otherwise.

            Whether the image should be stored as a progressive JPEG file.

            This parameter is deprecated.

        facecolor : color or 'auto', default: :rc:`savefig.facecolor`
            The facecolor of the figure.  If 'auto', use the current figure
            facecolor.

        edgecolor : color or 'auto', default: :rc:`savefig.edgecolor`
            The edgecolor of the figure.  If 'auto', use the current figure
            edgecolor.

        orientation : {'landscape', 'portrait'}
            Currently only supported by the postscript backend.

        papertype : str
            One of 'letter', 'legal', 'executive', 'ledger', 'a0' through
            'a10', 'b0' through 'b10'. Only supported for postscript
            output.

        format : str
            The file format, e.g. 'png', 'pdf', 'svg', ... The behavior when
            this is unset is documented under *fname*.

        transparent : bool
            If *True*, the Axes patches will all be transparent; the
            figure patch will also be transparent unless facecolor
            and/or edgecolor are specified via kwargs.
            This is useful, for example, for displaying
            a plot on top of a colored background on a web page.  The
            transparency of these patches will be restored to their
            original values upon exit of this function.

        bbox_inches : str or `.Bbox`, default: :rc:`savefig.bbox`
            Bounding box in inches: only the given portion of the figure is
            saved.  If 'tight', try to figure out the tight bbox of the figure.

        pad_inches : float, default: :rc:`savefig.pad_inches`
            Amount of padding around the figure when bbox_inches is 'tight'.

        bbox_extra_artists : list of `~matplotlib.artist.Artist`, optional
            A list of extra artists that will be considered when the
            tight bbox is calculated.

        backend : str, optional
            Use a non-default backend to render the file, e.g. to render a
            png file with the "cairo" backend rather than the default "agg",
            or a pdf file with the "pgf" backend rather than the default
            "pdf".  Note that the default backend is normally sufficient.  See
            :ref:`the-builtin-backends` for a list of valid backends for each
            file format.  Custom backends can be referenced as "module://...".

        metadata : dict, optional
            Key/value pairs to store in the image metadata. The supported keys
            and defaults depend on the image format and backend:

            - 'png' with Agg backend: See the parameter ``metadata`` of
              `~.FigureCanvasAgg.print_png`.
            - 'pdf' with pdf backend: See the parameter ``metadata`` of
              `~.backend_pdf.PdfPages`.
            - 'svg' with svg backend: See the parameter ``metadata`` of
              `~.FigureCanvasSVG.print_svg`.
            - 'eps' and 'ps' with PS backend: Only 'Creator' is supported.

        pil_kwargs : dict, optional
            Additional keyword arguments that are passed to
            `PIL.Image.Image.save` when saving the figure.
        """

        kwargs.setdefault('dpi', mpl.rcParams['savefig.dpi'])
        if transparent is None:
            transparent = mpl.rcParams['savefig.transparent']

        if transparent:
            kwargs.setdefault('facecolor', 'none')
            kwargs.setdefault('edgecolor', 'none')
            original_axes_colors = []
            for ax in self.axes:
                patch = ax.patch
                original_axes_colors.append((patch.get_facecolor(),
                                             patch.get_edgecolor()))
                patch.set_facecolor('none')
                patch.set_edgecolor('none')

        self.canvas.print_figure(fname, **kwargs)

        if transparent:
            for ax, cc in zip(self.axes, original_axes_colors):
                ax.patch.set_facecolor(cc[0])
                ax.patch.set_edgecolor(cc[1])

    def ginput(self, n=1, timeout=30, show_clicks=True,
               mouse_add=MouseButton.LEFT,
               mouse_pop=MouseButton.RIGHT,
               mouse_stop=MouseButton.MIDDLE):
        """
        Blocking call to interact with a figure.

        Wait until the user clicks *n* times on the figure, and return the
        coordinates of each click in a list.

        There are three possible interactions:

        - Add a point.
        - Remove the most recently added point.
        - Stop the interaction and return the points added so far.

        The actions are assigned to mouse buttons via the arguments
        *mouse_add*, *mouse_pop* and *mouse_stop*.

        Parameters
        ----------
        n : int, default: 1
            Number of mouse clicks to accumulate. If negative, accumulate
            clicks until the input is terminated manually.
        timeout : float, default: 30 seconds
            Number of seconds to wait before timing out. If zero or negative
            will never timeout.
        show_clicks : bool, default: True
            If True, show a red cross at the location of each click.
        mouse_add : `.MouseButton` or None, default: `.MouseButton.LEFT`
            Mouse button used to add points.
        mouse_pop : `.MouseButton` or None, default: `.MouseButton.RIGHT`
            Mouse button used to remove the most recently added point.
        mouse_stop : `.MouseButton` or None, default: `.MouseButton.MIDDLE`
            Mouse button used to stop input.

        Returns
        -------
        list of tuples
            A list of the clicked (x, y) coordinates.

        Notes
        -----
        The keyboard can also be used to select points in case your mouse
        does not have one or more of the buttons.  The delete and backspace
        keys act like right clicking (i.e., remove last point), the enter key
        terminates input and any other key (not already used by the window
        manager) selects a point.
        """
        blocking_mouse_input = BlockingMouseInput(self,
                                                  mouse_add=mouse_add,
                                                  mouse_pop=mouse_pop,
                                                  mouse_stop=mouse_stop)
        return blocking_mouse_input(n=n, timeout=timeout,
                                    show_clicks=show_clicks)

    def waitforbuttonpress(self, timeout=-1):
        """
        Blocking call to interact with the figure.

        Wait for user input and return True if a key was pressed, False if a
        mouse button was pressed and None if no input was given within
        *timeout* seconds.  Negative values deactivate *timeout*.
        """
        blocking_input = BlockingKeyMouseInput(self)
        return blocking_input(timeout=timeout)

    def init_layoutgrid(self):
        """Initialize the layoutgrid for use in constrained_layout."""
        del(self._layoutgrid)
        self._layoutgrid = layoutgrid.LayoutGrid(
            parent=None, name='figlb')

    def execute_constrained_layout(self, renderer=None):
        """
        Use ``layoutgrid`` to determine pos positions within Axes.

        See also `.set_constrained_layout_pads`.
        """

        from matplotlib._constrained_layout import do_constrained_layout
        from matplotlib.tight_layout import get_renderer

        _log.debug('Executing constrainedlayout')
        if self._layoutgrid is None:
            _api.warn_external("Calling figure.constrained_layout, but "
                               "figure not setup to do constrained layout. "
                               "You either called GridSpec without the "
                               "figure keyword, you are using plt.subplot, "
                               "or you need to call figure or subplots "
                               "with the constrained_layout=True kwarg.")
            return
        w_pad, h_pad, wspace, hspace = self.get_constrained_layout_pads()
        # convert to unit-relative lengths
        fig = self
        width, height = fig.get_size_inches()
        w_pad = w_pad / width
        h_pad = h_pad / height
        if renderer is None:
            renderer = get_renderer(fig)
        do_constrained_layout(fig, renderer, h_pad, w_pad, hspace, wspace)

    def tight_layout(self, *, pad=1.08, h_pad=None, w_pad=None, rect=None):
        """
        Adjust the padding between and around subplots.

        To exclude an artist on the Axes from the bounding box calculation
        that determines the subplot parameters (i.e. legend, or annotation),
        set ``a.set_in_layout(False)`` for that artist.

        Parameters
        ----------
        pad : float, default: 1.08
            Padding between the figure edge and the edges of subplots,
            as a fraction of the font size.
        h_pad, w_pad : float, default: *pad*
            Padding (height/width) between edges of adjacent subplots,
            as a fraction of the font size.
        rect : tuple (left, bottom, right, top), default: (0, 0, 1, 1)
            A rectangle in normalized figure coordinates into which the whole
            subplots area (including labels) will fit.

        See Also
        --------
        .Figure.set_tight_layout
        .pyplot.tight_layout
        """

        from .tight_layout import (
            get_renderer, get_subplotspec_list, get_tight_layout_figure)
        from contextlib import suppress
        subplotspec_list = get_subplotspec_list(self.axes)
        if None in subplotspec_list:
            _api.warn_external("This figure includes Axes that are not "
                               "compatible with tight_layout, so results "
                               "might be incorrect.")

        renderer = get_renderer(self)
        ctx = (renderer._draw_disabled()
               if hasattr(renderer, '_draw_disabled')
               else suppress())
        with ctx:
            kwargs = get_tight_layout_figure(
                self, self.axes, subplotspec_list, renderer,
                pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)
        if kwargs:
            self.subplots_adjust(**kwargs)
