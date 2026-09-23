    def configure_subplots(self, *args):
        global FigureManager  # placates pyflakes: created by @_Backend.export
        frame = wx.Frame(None, -1, "Configure subplots")
        _set_frame_icon(frame)

        toolfig = Figure((6, 3))
        canvas = type(self.canvas)(frame, -1, toolfig)

        # Create a figure manager to manage things
        FigureManager(canvas, 1, frame)

        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        frame.SetSizer(sizer)
        frame.Fit()
        SubplotTool(self.canvas.figure, toolfig)
        frame.Show()
