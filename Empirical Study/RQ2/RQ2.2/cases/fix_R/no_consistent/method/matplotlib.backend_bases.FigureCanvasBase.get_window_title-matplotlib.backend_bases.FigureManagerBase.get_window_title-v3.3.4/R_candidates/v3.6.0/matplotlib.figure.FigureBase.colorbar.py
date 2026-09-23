    @_docstring.dedent_interpd
    def colorbar(
            self, mappable, cax=None, ax=None, use_gridspec=True, **kwargs):
        """
        Add a colorbar to a plot.

        Parameters
        ----------
        mappable
            The `matplotlib.cm.ScalarMappable` (i.e., `.AxesImage`,
            `.ContourSet`, etc.) described by this colorbar.  This argument is
            mandatory for the `.Figure.colorbar` method but optional for the
            `.pyplot.colorbar` function, which sets the default to the current
            image.

            Note that one can create a `.ScalarMappable` "on-the-fly" to
            generate colorbars not attached to a previously drawn artist, e.g.
            ::

                fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)

        cax : `~matplotlib.axes.Axes`, optional
            Axes into which the colorbar will be drawn.

        ax : `~matplotlib.axes.Axes`, list of Axes, optional
            One or more parent axes from which space for a new colorbar axes
            will be stolen, if *cax* is None.  This has no effect if *cax* is
            set.

        use_gridspec : bool, optional
            If *cax* is ``None``, a new *cax* is created as an instance of
            Axes.  If *ax* is an instance of Subplot and *use_gridspec* is
            ``True``, *cax* is created as an instance of Subplot using the
            :mod:`.gridspec` module.

        Returns
        -------
        colorbar : `~matplotlib.colorbar.Colorbar`

        Other Parameters
        ----------------
        %(_make_axes_kw_doc)s
        %(_colormap_kw_doc)s

        Notes
        -----
        If *mappable* is a `~.contour.ContourSet`, its *extend* kwarg is
        included automatically.

        The *shrink* kwarg provides a simple way to scale the colorbar with
        respect to the axes. Note that if *cax* is specified, it determines the
        size of the colorbar and *shrink* and *aspect* kwargs are ignored.

        For more precise control, you can manually specify the positions of the
        axes objects in which the mappable and the colorbar are drawn.  In this
        case, do not use any of the axes properties kwargs.

        It is known that some vector graphics viewers (svg and pdf) renders
        white gaps between segments of the colorbar.  This is due to bugs in
        the viewers, not Matplotlib.  As a workaround, the colorbar can be
        rendered with overlapping segments::

            cbar = colorbar()
            cbar.solids.set_edgecolor("face")
            draw()

        However this has negative consequences in other circumstances, e.g.
        with semi-transparent images (alpha < 1) and colorbar extensions;
        therefore, this workaround is not used by default (see issue #1188).
        """

        if ax is None:
            ax = getattr(mappable, "axes", None)

        if (self.get_layout_engine() is not None and
                not self.get_layout_engine().colorbar_gridspec):
            use_gridspec = False
        # Store the value of gca so that we can set it back later on.
        if cax is None:
            if ax is None:
                raise ValueError(
                    'Unable to determine Axes to steal space for Colorbar. '
                    'Either provide the *cax* argument to use as the Axes for '
                    'the Colorbar, provide the *ax* argument to steal space '
                    'from it, or add *mappable* to an Axes.')
            current_ax = self.gca()
            userax = False
            if (use_gridspec and isinstance(ax, SubplotBase)):
                cax, kwargs = cbar.make_axes_gridspec(ax, **kwargs)
            else:
                cax, kwargs = cbar.make_axes(ax, **kwargs)
            cax.grid(visible=False, which='both', axis='both')
        else:
            userax = True

        # need to remove kws that cannot be passed to Colorbar
        NON_COLORBAR_KEYS = ['fraction', 'pad', 'shrink', 'aspect', 'anchor',
                             'panchor']
        cb_kw = {k: v for k, v in kwargs.items() if k not in NON_COLORBAR_KEYS}

        cb = cbar.Colorbar(cax, mappable, **cb_kw)

        if not userax:
            self.sca(current_ax)
        self.stale = True
        return cb
