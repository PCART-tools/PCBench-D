class FigureFrameWx(wx.Frame):
    def __init__(self, num, fig):
        # On non-Windows platform, explicitly set the position - fix
        # positioning bug on some Linux platforms
        if wx.Platform == '__WXMSW__':
            pos = wx.DefaultPosition
        else:
            pos = wx.Point(20, 20)
        l, b, w, h = fig.bbox.bounds
        wx.Frame.__init__(self, parent=None, id=-1, pos=pos,
                          title="Figure %d" % num)
        # Frame will be sized later by the Fit method
        DEBUG_MSG("__init__()", 1, self)
        self.num = num
        _set_frame_icon(self)

        self.canvas = self.get_canvas(fig)
        self.canvas.SetInitialSize(wx.Size(fig.bbox.width, fig.bbox.height))
        self.canvas.SetFocus()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        # By adding toolbar in sizer, we are able to put it at the bottom
        # of the frame - so appearance is closer to GTK version

        self.toolmanager = self._get_toolmanager()
        if self.toolmanager:
            self.statusbar = StatusbarWx(self, self.toolmanager)
        else:
            self.statusbar = StatusBarWx(self)
        self.SetStatusBar(self.statusbar)
        self.toolbar = self._get_toolbar(self.statusbar)

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
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

        # give the window a matplotlib icon rather than the stock one.
        # This is not currently working on Linux and is untested elsewhere.
        # icon_path = os.path.join(matplotlib.rcParams['datapath'],
        #                         'images', 'matplotlib.png')
        # icon = wx.IconFromBitmap(wx.Bitmap(icon_path))
        #  for xpm type icons try:
        # icon = wx.Icon(icon_path, wx.BITMAP_TYPE_XPM)
        #  self.SetIcon(icon)

        self.figmgr = FigureManagerWx(self.canvas, num, self)

        self.Bind(wx.EVT_CLOSE, self._onClose)

    def _get_toolbar(self, statbar):
        if rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2Wx(self.canvas)
            toolbar.set_status_bar(statbar)
        elif matplotlib.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarWx(self.toolmanager, self)
        else:
            toolbar = None
        return toolbar

    def _get_toolmanager(self):
        if matplotlib.rcParams['toolbar'] == 'toolmanager':
            toolmanager = ToolManager(self.canvas.figure)
        else:
            toolmanager = None
        return toolmanager

    def get_canvas(self, fig):
        return FigureCanvasWx(self, -1, fig)

    def get_figure_manager(self):
        DEBUG_MSG("get_figure_manager()", 1, self)
        return self.figmgr

    def _onClose(self, evt):
        DEBUG_MSG("onClose()", 1, self)
        self.canvas.close_event()
        self.canvas.stop_event_loop()
        Gcf.destroy(self.num)
        # self.Destroy()

    def GetToolBar(self):
        """Override wxFrame::GetToolBar as we don't have managed toolbar"""
        return self.toolbar

    def Destroy(self, *args, **kwargs):
        try:
            self.canvas.mpl_disconnect(self.toolbar._idDrag)
            # Rationale for line above: see issue 2941338.
        except AttributeError:
            pass  # classic toolbar lacks the attribute
        if not self.IsBeingDeleted():
            wx.Frame.Destroy(self, *args, **kwargs)
            if self.toolbar is not None:
                self.toolbar.Destroy()
            wxapp = wx.GetApp()
            if wxapp:
                wxapp.Yield()
        return True
