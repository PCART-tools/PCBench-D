class Colorbar(ColorbarBase):
    """
    This class connects a `ColorbarBase` to a `~.cm.ScalarMappable`
    such as an `~.image.AxesImage` generated via `~.axes.Axes.imshow`.

    .. note::
        This class is not intended to be instantiated directly; instead, use
        `.Figure.colorbar` or `.pyplot.colorbar` to create a colorbar.
    """

    def __init__(self, ax, mappable, **kwargs):
        # Ensure the given mappable's norm has appropriate vmin and vmax set
        # even if mappable.draw has not yet been called.
        if mappable.get_array() is not None:
            mappable.autoscale_None()

        self.mappable = mappable
        _add_disjoint_kwargs(kwargs, cmap=mappable.cmap, norm=mappable.norm)

        if isinstance(mappable, contour.ContourSet):
            cs = mappable
            _add_disjoint_kwargs(
                kwargs,
                alpha=cs.get_alpha(),
                boundaries=cs._levels,
                values=cs.cvalues,
                extend=cs.extend,
                filled=cs.filled,
            )
            kwargs.setdefault(
                'ticks', ticker.FixedLocator(cs.levels, nbins=10))
            super().__init__(ax, **kwargs)
            if not cs.filled:
                self.add_lines(cs)
        else:
            if getattr(mappable.cmap, 'colorbar_extend', False) is not False:
                kwargs.setdefault('extend', mappable.cmap.colorbar_extend)
            if isinstance(mappable, martist.Artist):
                _add_disjoint_kwargs(kwargs, alpha=mappable.get_alpha())
            super().__init__(ax, **kwargs)

        mappable.colorbar = self
        mappable.colorbar_cid = mappable.callbacksSM.connect(
            'changed', self.update_normal)

    @_api.deprecated("3.3", alternative="update_normal")
    def on_mappable_changed(self, mappable):
        """
        Update this colorbar to match the mappable's properties.

        Typically this is automatically registered as an event handler
        by :func:`colorbar_factory` and should not be called manually.
        """
        _log.debug('colorbar mappable changed')
        self.update_normal(mappable)

    def add_lines(self, CS, erase=True):
        """
        Add the lines from a non-filled `~.contour.ContourSet` to the colorbar.

        Parameters
        ----------
        CS : `~.contour.ContourSet`
            The line positions are taken from the ContourSet levels. The
            ContourSet must not be filled.
        erase : bool, default: True
            Whether to remove any previously added lines.
        """
        if not isinstance(CS, contour.ContourSet) or CS.filled:
            raise ValueError('add_lines is only for a ContourSet of lines')
        tcolors = [c[0] for c in CS.tcolors]
        tlinewidths = [t[0] for t in CS.tlinewidths]
        # Wishlist: Make colorbar lines auto-follow changes in contour lines.
        super().add_lines(CS.levels, tcolors, tlinewidths, erase=erase)

    def update_normal(self, mappable):
        """
        Update solid patches, lines, etc.

        This is meant to be called when the norm of the image or contour plot
        to which this colorbar belongs changes.

        If the norm on the mappable is different than before, this resets the
        locator and formatter for the axis, so if these have been customized,
        they will need to be customized again.  However, if the norm only
        changes values of *vmin*, *vmax* or *cmap* then the old formatter
        and locator will be preserved.
        """
        _log.debug('colorbar update normal %r %r', mappable.norm, self.norm)
        self.mappable = mappable
        self.set_alpha(mappable.get_alpha())
        self.cmap = mappable.cmap
        if mappable.norm != self.norm:
            self.norm = mappable.norm
            self._reset_locator_formatter_scale()

        self.draw_all()
        if isinstance(self.mappable, contour.ContourSet):
            CS = self.mappable
            if not CS.filled:
                self.add_lines(CS)
        self.stale = True

    @_api.deprecated("3.3", alternative="update_normal")
    def update_bruteforce(self, mappable):
        """
        Destroy and rebuild the colorbar.  This is
        intended to become obsolete, and will probably be
        deprecated and then removed.  It is not called when
        the pyplot.colorbar function or the Figure.colorbar
        method are used to create the colorbar.
        """
        # We are using an ugly brute-force method: clearing and
        # redrawing the whole thing.  The problem is that if any
        # properties have been changed by methods other than the
        # colorbar methods, those changes will be lost.
        self.ax.cla()
        self.locator = None
        self.formatter = None

        # clearing the axes will delete outline, patch, solids, and lines:
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.outline = self.ax.spines['outline'] = _ColorbarSpine(self.ax)
        self.patch = mpatches.Polygon(
            np.empty((0, 2)),
            color=mpl.rcParams['axes.facecolor'], linewidth=0.01, zorder=-1)
        self.ax.add_artist(self.patch)
        self.solids = None
        self.lines = []
        self.update_normal(mappable)
        self.draw_all()
        if isinstance(self.mappable, contour.ContourSet):
            CS = self.mappable
            if not CS.filled:
                self.add_lines(CS)
            #if self.lines is not None:
            #    tcolors = [c[0] for c in CS.tcolors]
            #    self.lines.set_color(tcolors)
        #Fixme? Recalculate boundaries, ticks if vmin, vmax have changed.
        #Fixme: Some refactoring may be needed; we should not
        # be recalculating everything if there was a simple alpha
        # change.

    def remove(self):
        """
        Remove this colorbar from the figure.

        If the colorbar was created with ``use_gridspec=True`` the previous
        gridspec is restored.
        """
        super().remove()
        self.mappable.callbacksSM.disconnect(self.mappable.colorbar_cid)
        self.mappable.colorbar = None
        self.mappable.colorbar_cid = None

        try:
            ax = self.mappable.axes
        except AttributeError:
            return

        try:
            gs = ax.get_subplotspec().get_gridspec()
            subplotspec = gs.get_topmost_subplotspec()
        except AttributeError:
            # use_gridspec was False
            pos = ax.get_position(original=True)
            ax._set_position(pos)
        else:
            # use_gridspec was True
            ax.set_subplotspec(subplotspec)
