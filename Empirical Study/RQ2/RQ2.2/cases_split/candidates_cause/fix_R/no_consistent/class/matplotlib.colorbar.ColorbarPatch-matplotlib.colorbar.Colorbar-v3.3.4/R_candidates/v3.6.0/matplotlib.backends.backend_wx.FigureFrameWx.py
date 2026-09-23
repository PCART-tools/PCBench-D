class FigureFrameWx(wx.Frame):
    def __init__(self, num, fig, *, canvas_class=None):
        # On non-Windows platform, explicitly set the position - fix
        # positioning bug on some Linux platforms
        if wx.Platform == '__WXMSW__':
            pos = wx.DefaultPosition
        else:
            pos = wx.Point(20, 20)
        super().__init__(parent=None, id=-1, pos=pos)
        # Frame will be sized later by the Fit method
        _log.debug("%s - __init__()", type(self))
        _set_frame_icon(self)

        # The parameter will become required after the deprecation elapses.
        if canvas_class is not None:
            self.canvas = canvas_class(self, -1, fig)
        else:
            _api.warn_deprecated(
                "3.6", message="The canvas_class parameter will become "
                "required after the deprecation period starting in Matplotlib "
                "%(since)s elapses.")
            self.canvas = self.get_canvas(fig)

        # Auto-attaches itself to self.canvas.manager
        manager = FigureManagerWx(self.canvas, num, self)

        toolbar = self.canvas.manager.toolbar
        if toolbar is not None:
            self.SetToolBar(toolbar)

        # On Windows, canvas sizing must occur after toolbar addition;
        # otherwise the toolbar further resizes the canvas.
        w, h = map(math.ceil, fig.bbox.size)
        self.canvas.SetInitialSize(wx.Size(w, h))
        self.canvas.SetMinSize((2, 2))
        self.canvas.SetFocus()

        self.Fit()

        self.Bind(wx.EVT_CLOSE, self._on_close)

    sizer = _api.deprecated("3.6", alternative="frame.GetSizer()")(
        property(lambda self: self.GetSizer()))
    figmgr = _api.deprecated("3.6", alternative="frame.canvas.manager")(
        property(lambda self: self.canvas.manager))
    num = _api.deprecated("3.6", alternative="frame.canvas.manager.num")(
        property(lambda self: self.canvas.manager.num))
    toolbar = _api.deprecated("3.6", alternative="frame.GetToolBar()")(
        property(lambda self: self.GetToolBar()))
    toolmanager = _api.deprecated(
        "3.6", alternative="frame.canvas.manager.toolmanager")(
            property(lambda self: self.canvas.manager.toolmanager))

    @_api.deprecated(
        "3.6", alternative="the canvas_class constructor parameter")
    def get_canvas(self, fig):
        return FigureCanvasWx(self, -1, fig)

    @_api.deprecated("3.6", alternative="frame.canvas.manager")
    def get_figure_manager(self):
        _log.debug("%s - get_figure_manager()", type(self))
        return self.canvas.manager

    def _on_close(self, event):
        _log.debug("%s - on_close()", type(self))
        CloseEvent("close_event", self.canvas)._process()
        self.canvas.stop_event_loop()
        # set FigureManagerWx.frame to None to prevent repeated attempts to
        # close this frame from FigureManagerWx.destroy()
        self.canvas.manager.frame = None
        # remove figure manager from Gcf.figs
        Gcf.destroy(self.canvas.manager)
        try:  # See issue 2941338.
            self.canvas.mpl_disconnect(self.canvas.toolbar._id_drag)
        except AttributeError:  # If there's no toolbar.
            pass
        # Carry on with close event propagation, frame & children destruction
        event.Skip()
