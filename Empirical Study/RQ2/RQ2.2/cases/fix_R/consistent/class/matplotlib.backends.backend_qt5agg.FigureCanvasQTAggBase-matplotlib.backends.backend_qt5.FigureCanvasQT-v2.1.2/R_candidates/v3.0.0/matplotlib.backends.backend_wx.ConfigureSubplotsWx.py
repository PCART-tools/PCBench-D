class ConfigureSubplotsWx(backend_tools.ConfigureSubplotsBase):
    def trigger(self, *args):
        self.configure_subplots()

    def configure_subplots(self):
        frame = wx.Frame(None, -1, "Configure subplots")
        _set_frame_icon(frame)

        toolfig = Figure((6, 3))
        canvas = self.get_canvas(frame, toolfig)

        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        frame.SetSizer(sizer)
        frame.Fit()
        tool = SubplotTool(self.canvas.figure, toolfig)
        frame.Show()

    def get_canvas(self, frame, fig):
        return type(self.canvas)(frame, -1, fig)
