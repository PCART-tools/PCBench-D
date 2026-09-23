    def resize(self, width, height):
        # docstring inherited
        self.canvas.SetInitialSize(wx.Size(width, height))
        self.window.GetSizer().Fit(self.window)
