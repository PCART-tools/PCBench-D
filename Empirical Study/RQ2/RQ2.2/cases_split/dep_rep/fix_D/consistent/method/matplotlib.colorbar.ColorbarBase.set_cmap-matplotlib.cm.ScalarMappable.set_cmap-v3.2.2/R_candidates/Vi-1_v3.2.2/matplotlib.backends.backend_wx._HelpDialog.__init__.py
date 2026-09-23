    def __init__(self, parent, help_entries):
        wx.Dialog.__init__(self, parent, title="Help",
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.FlexGridSizer(0, 3, 8, 6)
        # create and add the entries
        bold = self.GetFont().MakeBold()
        for r, row in enumerate(self.headers + help_entries):
            for (col, width) in zip(row, self.widths):
                label = wx.StaticText(self, label=col)
                if r == 0:
                    label.SetFont(bold)
                label.Wrap(width)
                grid_sizer.Add(label, 0, 0, 0)
        # finalize layout, create button
        sizer.Add(grid_sizer, 0, wx.ALL, 6)
        OK = wx.Button(self, wx.ID_OK)
        sizer.Add(OK, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 8)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        OK.Bind(wx.EVT_BUTTON, self.OnClose)
