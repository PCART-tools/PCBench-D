    def __init__(self, canvas, coordinates=True, *, style=wx.TB_BOTTOM):
        wx.ToolBar.__init__(self, canvas.GetParent(), -1, style=style)
        if wx.Platform == '__WXMAC__':
            self.SetToolBitmapSize(self.GetToolBitmapSize()*self.GetDPIScaleFactor())

        self.wx_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.AddSeparator()
                continue
            self.wx_ids[text] = (
                self.AddTool(
                    -1,
                    bitmap=self._icon(f"{image_file}.svg"),
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
            self._label_text = wx.StaticText(self, style=wx.ALIGN_RIGHT)
            self.AddControl(self._label_text)

        self.Realize()

        NavigationToolbar2.__init__(self, canvas)
