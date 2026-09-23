    def select(self):
        """Select the current bitmap into this wxDC instance."""
        if sys.platform == 'win32':
            self.dc.SelectObject(self.bitmap)
            self.IsSelected = True
