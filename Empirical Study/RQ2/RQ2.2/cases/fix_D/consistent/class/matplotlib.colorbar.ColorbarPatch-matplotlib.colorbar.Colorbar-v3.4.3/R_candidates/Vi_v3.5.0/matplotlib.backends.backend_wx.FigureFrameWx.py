class FigureFrameWx(wx.Frame):
    def __init__(self, num, fig):
        # On non-Windows platform, explicitly set the position - fix
        # positioning bug on some Linux platforms
        if wx.Platform == '__WXMSW__':
            pos = wx.DefaultPosition
        else:
            pos = wx.Point(20, 20)
        super().__init__(parent=None, id=-1, pos=pos)
        # Frame will be sized later by the Fit method
        _log.debug("%s - __init__()", type(self))
        self.num = num
        _set_frame_icon(self)

        self.canvas = self.get_canvas(fig)
        w, h = map(math.ceil, fig.bbox.size)
        self.canvas.SetInitialSize(wx.Size(w, h))
        self.canvas.SetFocus()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        # By adding toolbar in sizer, we are able to put it at the bottom
        # of the frame - so appearance is closer to GTK version

        self.figmgr = FigureManagerWx(self.canvas, num, self)

        self.toolbar = self._get_toolbar()

        if self.figmgr.toolmanager:
            backend_tools.add_tools_to_manager(self.figmgr.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)

        if self.toolbar is not None:
            self.toolbar.Realize()
            # On Windows platform, default window size is incorrect, so set
            # toolbar width to figure width.
            tw, th = self.toolbar.GetSize()
            fw, fh = self.canvas.GetSize()
            # By adding toolbar in sizer, we are able to put it at the bottom
            # of the frame - so appearance is closer to GTK version.
            self.toolbar.SetSize(wx.Size(fw, th))
            self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.canvas.SetMinSize((2, 2))

        self.Bind(wx.EVT_CLOSE, self._onClose)

    @property
    def toolmanager(self):
        return self.figmgr.toolmanager

    def _get_toolbar(self):
        if mpl.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Wx(self.canvas)
        elif mpl.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarWx(self.toolmanager, self)
        else:
            toolbar = None
        return toolbar

    def get_canvas(self, fig):
        return FigureCanvasWx(self, -1, fig)

    def get_figure_manager(self):
        _log.debug("%s - get_figure_manager()", type(self))
        return self.figmgr

    def _onClose(self, event):
        _log.debug("%s - onClose()", type(self))
        self.canvas.close_event()
        self.canvas.stop_event_loop()
        # set FigureManagerWx.frame to None to prevent repeated attempts to
        # close this frame from FigureManagerWx.destroy()
        self.figmgr.frame = None
        # remove figure manager from Gcf.figs
        Gcf.destroy(self.figmgr)
        # Carry on with close event propagation, frame & children destruction
        event.Skip()

    def GetToolBar(self):
        """Override wxFrame::GetToolBar as we don't have managed toolbar"""
        return self.toolbar

    def Destroy(self, *args, **kwargs):
        try:
            self.canvas.mpl_disconnect(self.toolbar._id_drag)
            # Rationale for line above: see issue 2941338.
        except AttributeError:
            pass  # classic toolbar lacks the attribute
        # The "if self" check avoids a "wrapped C/C++ object has been deleted"
        # RuntimeError at exit with e.g.
        # MPLBACKEND=wxagg python -c 'from pylab import *; plot()'.
        if self and not self.IsBeingDeleted():
            super().Destroy(*args, **kwargs)
            # self.toolbar.Destroy() should not be necessary if the close event
            # is allowed to propagate.
        return True
