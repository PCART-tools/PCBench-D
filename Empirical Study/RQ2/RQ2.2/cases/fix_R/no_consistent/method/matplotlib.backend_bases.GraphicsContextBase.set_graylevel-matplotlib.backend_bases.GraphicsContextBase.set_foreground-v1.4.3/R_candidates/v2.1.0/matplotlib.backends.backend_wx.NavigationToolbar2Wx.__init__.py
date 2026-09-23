    def __init__(self, canvas):
        wx.ToolBar.__init__(self, canvas.GetParent(), -1)
        NavigationToolbar2.__init__(self, canvas)
        self.canvas = canvas
        self._idle = True
        self.statbar = None
        self.prevZoomRect = None
        # for now, use alternate zoom-rectangle drawing on all
        # Macs. N.B. In future versions of wx it may be possible to
        # detect Retina displays with window.GetContentScaleFactor()
        # and/or dc.GetContentScaleFactor()
        self.retinaFix = 'wxMac' in wx.PlatformInfo
