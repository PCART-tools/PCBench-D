    def resize(self, width, height):
        # docstring inherited
        # Directly using SetClientSize doesn't handle the toolbar on Windows.
        self.window.SetSize(self.window.ClientToWindowSize(wx.Size(
            math.ceil(width), math.ceil(height))))
