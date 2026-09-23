    def _mpl_coords(self, pos=None):
        """
        Convert a wx position, defaulting to the current cursor position, to
        Matplotlib coordinates.
        """
        if pos is None:
            pos = wx.GetMouseState()
            x, y = self.ScreenToClient(pos.X, pos.Y)
        else:
            x, y = pos.X, pos.Y
        # flip y so y=0 is bottom of canvas
        if not wx.Platform == '__WXMSW__':
            scale = self.GetDPIScaleFactor()
            return x*scale, self.figure.bbox.height - y*scale
        else:
            return x, self.figure.bbox.height - y
