    def __init__(self, targetfig):
        wx.Frame.__init__(self, None, -1, "Configure subplots")

        toolfig = Figure((6, 3))
        canvas = FigureCanvasWx(self, -1, toolfig)

        # Create a figure manager to manage things
        figmgr = FigureManager(canvas, 1, self)

        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(sizer)
        self.Fit()
        tool = SubplotTool(targetfig, toolfig)
