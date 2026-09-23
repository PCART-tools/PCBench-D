    def __init__(self, canvas, coordinates=True):
        wx.ToolBar.__init__(self, canvas.GetParent(), -1)

        if 'wxMac' in wx.PlatformInfo:
            self.SetToolBitmapSize((24, 24))
        self.wx_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.AddSeparator()
                continue
            self.wx_ids[text] = (
                self.AddTool(
                    -1,
                    bitmap=self._icon(f"{image_file}.png"),
                    bmpDisabled=wx.NullBitmap,
                    label=text, shortHelp=tooltip_text,
                    kind=(wx.ITEM_CHECK if text in ["Pan", "Zoom"]
                          else wx.ITEM_NORMAL))
                .Id)
            self.Bind(wx.EVT_TOOL, getattr(self, callback),
                      id=self.wx_ids[text])

        self._coordinates = coordinates
        if self._coordinates:
            self.AddStretchableSpace()
            self._label_text = wx.StaticText(self)
            self.AddControl(self._label_text)

        self.Realize()

        NavigationToolbar2.__init__(self, canvas)

        self._prevZoomRect = None
        # for now, use alternate zoom-rectangle drawing on all
        # Macs. N.B. In future versions of wx it may be possible to
        # detect Retina displays with window.GetContentScaleFactor()
        # and/or dc.GetContentScaleFactor()
        self._retinaFix = 'wxMac' in wx.PlatformInfo
