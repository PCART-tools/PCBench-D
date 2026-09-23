    def unselect(self):
        """Select a Null bitmap into this wxDC instance."""
        if sys.platform == 'win32':
            self.dc.SelectObject(wx.NullBitmap)
            self.IsSelected = False
