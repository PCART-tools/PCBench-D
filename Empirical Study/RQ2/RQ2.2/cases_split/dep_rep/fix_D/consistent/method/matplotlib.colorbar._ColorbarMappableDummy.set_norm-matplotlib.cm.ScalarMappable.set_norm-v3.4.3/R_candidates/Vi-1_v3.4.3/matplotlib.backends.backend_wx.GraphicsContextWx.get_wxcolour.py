    def get_wxcolour(self, color):
        """Convert a RGB(A) color to a wx.Colour."""
        _log.debug("%s - get_wx_color()", type(self))
        return wx.Colour(*[int(255 * x) for x in color])
