    def resize(self, width, height):
        # docstring inherited
        self.canvas.SetInitialSize(
            wx.Size(math.ceil(width), math.ceil(height)))
        self.window.GetSizer().Fit(self.window)
