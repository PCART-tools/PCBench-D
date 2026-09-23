    def unselect(self):
        """
        Select a Null bitmasp into this wxDC instance
        """
        if sys.platform == 'win32':
            self.dc.SelectObject(wx.NullBitmap)
            self.IsSelected = False
