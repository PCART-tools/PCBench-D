    def resize(self, width, height):
        'Set the canvas size in pixels'
        self.canvas.SetInitialSize(wx.Size(width, height))
        self.window.GetSizer().Fit(self.window)
