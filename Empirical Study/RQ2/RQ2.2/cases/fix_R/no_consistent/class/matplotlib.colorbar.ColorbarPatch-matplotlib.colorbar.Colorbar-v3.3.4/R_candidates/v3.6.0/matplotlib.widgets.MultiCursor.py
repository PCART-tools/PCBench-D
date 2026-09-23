class MultiCursor(Widget):
    """
    Provide a vertical (default) and/or horizontal line cursor shared between
    multiple Axes.

    For the cursor to remain responsive you must keep a reference to it.

    Parameters
    ----------
    canvas : object
        This parameter is entirely unused and only kept for back-compatibility.

    axes : list of `matplotlib.axes.Axes`
        The `~.axes.Axes` to attach the cursor to.

    useblit : bool, default: True
        Use blitting for faster drawing if supported by the backend.
        See the tutorial :doc:`/tutorials/advanced/blitting`
        for details.

    horizOn : bool, default: False
        Whether to draw the horizontal line.

    vertOn : bool, default: True
        Whether to draw the vertical line.

    Other Parameters
    ----------------
    **lineprops
        `.Line2D` properties that control the appearance of the lines.
        See also `~.Axes.axhline`.

    Examples
    --------
    See :doc:`/gallery/widgets/multicursor`.
    """

    @_api.make_keyword_only("3.6", "useblit")
    def __init__(self, canvas, axes, useblit=True, horizOn=False, vertOn=True,
                 **lineprops):
        # canvas is stored only to provide the deprecated .canvas attribute;
        # once it goes away the unused argument won't need to be stored at all.
        self._canvas = canvas

        self.axes = axes
        self.horizOn = horizOn
        self.vertOn = vertOn

        self._canvas_infos = {
            ax.figure.canvas: {"cids": [], "background": None} for ax in axes}

        xmin, xmax = axes[-1].get_xlim()
        ymin, ymax = axes[-1].get_ylim()
        xmid = 0.5 * (xmin + xmax)
        ymid = 0.5 * (ymin + ymax)

        self.visible = True
        self.useblit = (
            useblit
            and all(canvas.supports_blit for canvas in self._canvas_infos))
        self.needclear = False

        if self.useblit:
            lineprops['animated'] = True

        if vertOn:
            self.vlines = [ax.axvline(xmid, visible=False, **lineprops)
                           for ax in axes]
        else:
            self.vlines = []

        if horizOn:
            self.hlines = [ax.axhline(ymid, visible=False, **lineprops)
                           for ax in axes]
        else:
            self.hlines = []

        self.connect()

    canvas = _api.deprecate_privatize_attribute("3.6")
    background = _api.deprecated("3.6")(lambda self: (
        self._backgrounds[self.axes[0].figure.canvas] if self.axes else None))

    def connect(self):
        """Connect events."""
        for canvas, info in self._canvas_infos.items():
            info["cids"] = [
                canvas.mpl_connect('motion_notify_event', self.onmove),
                canvas.mpl_connect('draw_event', self.clear),
            ]

    def disconnect(self):
        """Disconnect events."""
        for canvas, info in self._canvas_infos.items():
            for cid in info["cids"]:
                canvas.mpl_disconnect(cid)
            info["cids"].clear()

    def clear(self, event):
        """Clear the cursor."""
        if self.ignore(event):
            return
        if self.useblit:
            for canvas, info in self._canvas_infos.items():
                info["background"] = canvas.copy_from_bbox(canvas.figure.bbox)
        for line in self.vlines + self.hlines:
            line.set_visible(False)

    def onmove(self, event):
        if (self.ignore(event)
                or event.inaxes not in self.axes
                or not event.canvas.widgetlock.available(self)):
            return
        self.needclear = True
        if not self.visible:
            return
        if self.vertOn:
            for line in self.vlines:
                line.set_xdata((event.xdata, event.xdata))
                line.set_visible(self.visible)
        if self.horizOn:
            for line in self.hlines:
                line.set_ydata((event.ydata, event.ydata))
                line.set_visible(self.visible)
        self._update()

    def _update(self):
        if self.useblit:
            for canvas, info in self._canvas_infos.items():
                if info["background"]:
                    canvas.restore_region(info["background"])
            if self.vertOn:
                for ax, line in zip(self.axes, self.vlines):
                    ax.draw_artist(line)
            if self.horizOn:
                for ax, line in zip(self.axes, self.hlines):
                    ax.draw_artist(line)
            for canvas in self._canvas_infos:
                canvas.blit()
        else:
            for canvas in self._canvas_infos:
                canvas.draw_idle()
